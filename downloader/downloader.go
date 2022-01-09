package downloader

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

const DownloadBasePath = "images"

// Downloader 下载器
// UrlList 任务列表
type Downloader struct {
	UrlList []string
}

func init() {
	// 初始化目录
	_ = os.Mkdir(DownloadBasePath, 0777)
}

// New 构造一个下载器
func New(taskList []string) (manager *Downloader) {
	manager = &Downloader{
		UrlList: taskList,
	}
	return
}

// Start 开始任务
func (manager *Downloader) Start() {
	urlCount := len(manager.UrlList)
	urlCompleteCount := 0
	for _, url := range manager.UrlList {
		log.Printf(":任务开始: :url: %s\n", url)
		manager.download(url)
		urlCompleteCount += 1
		log.Printf(":任务完成: :url: %s %d/%d\n", url, urlCompleteCount, urlCount)
	}
}

// download 下载
func (manager *Downloader) download(url string) {
	for {
		response, err := http.Get(url)
		checkError(err)

		responseStatusCode := response.StatusCode
		log.Println(":downloader():", ":url:", url, ":responseStatusCode:", responseStatusCode)
		if responseStatusCode != 200 {
			log.Println(":downloader():", ":url:", url, "retry...")
			time.Sleep(time.Second * 2)
			continue
		}

		urlSplit := strings.Split(url, "/")
		filename := urlSplit[len(urlSplit)-1]

		file, err := os.Create(DownloadBasePath + "/" + filename)
		checkError(err)

		bytes, _ := ioutil.ReadAll(response.Body)
		_, _ = file.Write(bytes)

		_ = response.Body.Close()
		_ = file.Close()

		break
	}
}

func checkError(err error) {
	if err != nil {
		log.Println(err)
	}
}
