package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"astuart.co/goq"
)

type Wiki struct {
	Title   string   `goquery:"h1"`
	Content []string `goquery:"div.mw-parser-output p"`
}

func main() {

	kw := "Logistic Regression"
	w := wiki(kw)

	if len(w.Content) >= 3 {
		w.Content = w.Content[0:3]
	}
	fmt.Println(PrettyPrint(w))
}

// PrettyPrint to print struct in a readable way
func PrettyPrint(i interface{}) string {
	s, _ := json.MarshalIndent(i, "", "\t")
	return string(s)
}

func wiki(keyword string) Wiki {

	// construct wiki links
	link := fmt.Sprintf("https://en.wikipedia.org/wiki/%s", keyword)

	res, err := http.Get(link)
	if err != nil {
		fmt.Println(err)
	}
	defer res.Body.Close()

	var wiki Wiki
	err = goq.NewDecoder(res.Body).Decode(&wiki)
	if err != nil {
		fmt.Println(err)
	}

	return wiki
}
