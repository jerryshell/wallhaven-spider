package download

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

const BasePath = "images"

// Manager 下载管理器
// UrlList 任务列表
// taskCompleteChan 任务完成信道
type Manager struct {
	UrlList []string
}

func init() {
	// 初始化目录
	_ = os.Mkdir(BasePath, 0777)
}

// NewManager 构造一个下载管理器
func NewManager(tasks []string) (manager *Manager) {
	manager = &Manager{
		UrlList: tasks,
	}
	return
}

// Start 开始任务
func (manager *Manager) Start() {
	taskCount := len(manager.UrlList)
	taskCompleteCount := 0
	for _, url := range manager.UrlList {
		log.Printf(":任务开始:%s\n", url)
		manager.download(url)
		taskCompleteCount += 1
		log.Printf(":任务完成:%d/%d:%s\n", taskCompleteCount, taskCount, url)
	}
}

// download 下载
func (manager *Manager) download(url string) {
	for {
		response, err := http.Get(url)
		checkError(err)

		responseStatusCode := response.StatusCode
		log.Println(":download():", ":url:", url, ":responseStatusCode:", responseStatusCode)
		if responseStatusCode != 200 {
			log.Println(":download():", ":url:", url, "retry...")
			time.Sleep(time.Second * 2)
			continue
		}

		urlSplit := strings.Split(url, "/")
		filename := urlSplit[len(urlSplit)-1]

		file, err := os.Create(BasePath + "/" + filename)
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
