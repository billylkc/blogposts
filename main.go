package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"astuart.co/goq"
)

// Article as a struct to parse Openrice Article
type Article struct {
	Title   string   `goquery:"div.cms-detail-title.or-font-family"`
	Content []string `goquery:"div.cms-detail-body-text div"`
}

func main() {
	// Random promotion link from the front page. May be going to be expired
	link := "https://www.openrice.com/zh/hongkong/promo/%E3%80%90%E7%B5%82%E6%96%BC%E7%B4%84friend%E9%A3%9F%E9%A3%AF%E3%80%91%E5%B0%96%E6%B2%99%E5%92%80%E4%B8%BB%E6%89%93%E9%A3%B2%E9%85%92%E6%B5%B7%E9%AE%AE-outdoor%E4%BD%8D%E6%9C%89%E6%B0%A3%E6%B0%9B-a5816"
	result := getArticle(link)

	fmt.Println(PrettyPrint(result))
}

// PrettyPrint to print struct in a readable way
func PrettyPrint(i interface{}) string {
	s, _ := json.MarshalIndent(i, "", "\t")
	return string(s)
}

// getArticle parses the input link and extract the content of the article
// We are passing the link as argument this time
func getArticle(link string) Article {
	res, err := http.Get(link)
	if err != nil {
		fmt.Println(err)
	}
	defer res.Body.Close()

	var rice Article
	err = goq.NewDecoder(res.Body).Decode(&rice)
	if err != nil {
		fmt.Println(err)
	}

	return rice
}
