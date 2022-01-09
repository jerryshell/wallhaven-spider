package spider

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"github.com/jerryshell/wallhaven-spider/download"
	"log"
	"net/http"
	"time"
)

// Get24Image 获取 24 张图片
func Get24Image() {
	log.Println(":分析页面:")

	imageUrlList := getImageUrlList()

	downloadManager := download.NewManager(imageUrlList)
	downloadManager.Start()
}

// Get24NImage 获取 24*n 张图片
func Get24NImage() {
	var n int
	for {
		fmt.Print("即将获取 24*N 张图片，请输入 N\n>>> ")
		_, err := fmt.Scanf("%d", &n)
		if err != nil {
			checkError(err)
		}
		if n <= 0 {
			fmt.Println("N 必须大于 0")
			continue
		}
		break
	}

	for i := 0; i < n; i++ {
		log.Printf("开始第 %d 次任务\n", i+1)
		Get24Image()
	}
}

func getDoc(url string) *goquery.Document {
	for {
		response, err := http.Get(url)
		checkError(err)

		responseStatusCode := response.StatusCode
		log.Println(":getDoc():", ":url:", url, ":responseStatusCode:", responseStatusCode)
		if responseStatusCode != 200 {
			time.Sleep(time.Second * 2)
			continue
		}

		doc, err := goquery.NewDocumentFromReader(response.Body)
		checkError(err)

		_ = response.Body.Close()

		return doc
	}
}

func getPageUrlList() (hrefSlice []string) {
	doc := getDoc("https://wallhaven.cc/random")
	doc.Find("a.preview").Each(func(i int, s *goquery.Selection) {
		href, exists := s.Attr("href")
		if !exists {
			return
		}

		hrefSlice = append(hrefSlice, href)
	})
	return
}

func getImageUrlByPageUrl(pageUrl string) (imageUrl string) {
	doc := getDoc(pageUrl)
	element := doc.Find("#wallpaper")
	imageUrl, _ = element.Attr("src")
	log.Println(":getImageUrlByPageUrl():", ":pageUrl:", pageUrl, ":imageUrl:", imageUrl)
	return
}

func getImageUrlList() []string {
	pageUrlList := getPageUrlList()
	imageUrlList := make([]string, 0)
	for _, pageUrl := range pageUrlList {
		imageURL := getImageUrlByPageUrl(pageUrl)
		imageUrlList = append(imageUrlList, imageURL)
	}
	return imageUrlList
}

func checkError(err error) {
	if err != nil {
		log.Println(err)
	}
}
