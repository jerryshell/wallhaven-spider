package download

import (
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

var downloadDir = "./images"

// Manager 下载管理器
// Tasks 任务列表
// taskCompleteChan 任务完成信道
type Manager struct {
	Tasks []string
}

func init() {
	// 初始化目录
	_ = os.Mkdir(downloadDir, 0777)
}

// NewManager 构造一个下载管理器
func NewManager(tasks []string) (manager *Manager) {
	manager = &Manager{
		Tasks: tasks,
	}
	return
}

// Start 开始任务
func (manager *Manager) Start() {
	taskNumber := len(manager.Tasks)
	taskCompleteNumber := 0
	for _, url := range manager.Tasks {
		log.Printf(":任务开始:%s\n", url)
		manager.download(url)
		taskCompleteNumber += 1
		log.Printf(":任务完成:%d/%d:%s\n", taskCompleteNumber, taskNumber, url)
	}
}

func (manager *Manager) download(url string) {
	res, err := http.Get(url)
	checkError(err)
	defer func(Body io.ReadCloser) {
		_ = Body.Close()
	}(res.Body)

	fileNameSplit := strings.Split(url, "/")
	fileName := fileNameSplit[len(fileNameSplit)-1]
	file, err := os.Create(downloadDir + "/" + fileName)
	checkError(err)
	defer func(file *os.File) {
		_ = file.Close()
	}(file)

	buf := make([]byte, 100*1024)
	for {
		n, err := res.Body.Read(buf)
		if n == 0 {
			break
		}
		if err != io.EOF {
			checkError(err)
		}

		_, _ = file.Write(buf[:n])
	}
}

func checkError(err error) {
	if err != nil {
		log.Println(err)
	}
}
