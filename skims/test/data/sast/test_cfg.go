package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

type Class struct{}

func (this *Class) CapturePanic(h httprouter.Handle) {
	var err error
	r := recover()
	if r != nil {
		switch t := r.(type) {  // Missing Case switch
		case string:  // Missing Case case
			err = errors.New(t)
		case error:  // Missing Case case
			err = t
		default:  // Missing Case default
			err = errors.New("Unknown error")
		}
		log.Println(err.Error())
		http.Error(w, err.Error(), http.StatusInternalServerError)  // Missing Case selector_expression
	}
}

func (this *Class) DetectSQLMap(h httprouter.Handle) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {   // Missing Case func_literal
		userAgent := r.Header.Get("User-Agent")
		sqlmapDetected, _ := regexp.MatchString("sqlmap*", userAgent)
		if sqlmapDetected {
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden"))
			log.Printf("sqlmap detect ")
			return
		} else {
			h(w, r, ps)
		}
	}
}

func (this *Class) AuthCheck(h httprouter.Handle) httprouter.Handle {
	var sess = session.New()
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {   // Missing Case func_literal
		if !sess.IsLoggedIn(r) {
			redirect := "/login"
			http.Redirect(w, r, redirect, http.StatusSeeOther)
			return
		}

		h(w, r, ps)
	}
}

type Profile struct {
	Uid         int
	Name        string
	City        string
	PhoneNumber string
}

func (p *Profile) UnsafeQueryGetData(uid string) error {

	/* this funciton use to get data Profile from database with vulnerable query */
	DB, err = database.Connect()

	getProfileSql := fmt.Sprintf(`SELECT p.user_id, p.full_name, p.city, p.phone_number
								FROM Profile as p,Users as u
								where p.user_id = u.id
								and u.id=%s`, uid) //here is the vulnerable query
	rows, err := DB.Query(getProfileSql)
	if err != nil {
		return err //this will return error query to clien hmmmm.
	}
	defer rows.Close()  // Missing Case defer
	//var profile = Profile{}
	for rows.Next() {  // Missing Case for_statement
		err = rows.Scan(&p.Uid, &p.Name, &p.City, &p.PhoneNumber)  // Missing Case unary_expression
		if err != nil {
			log.Printf("Row scan error: %s", err.Error())
			return err
		}
	}
	return nil
}

func (p *Profile) SafeQueryGetData(uid string) error {

	/* this funciton use to get data Profile from database with prepare statement */
	DB, err = database.Connect()

	const (
		getProfileSql = `SELECT p.user_id, p.full_name, p.city, p.phone_number
		FROM Profile as p,Users as u
		where p.user_id = u.id
		and u.id=?`
	)

	stmt, err := DB.Prepare(getProfileSql) //prepare statement
	if err != nil {
		return err
	}

	defer stmt.Close()  // Missing Case defer
	err = stmt.QueryRow(uid).Scan(&p.Uid, &p.Name, &p.City, &p.PhoneNumber)  // Missing Case unary_expression
	if err != nil {
		return err
	}
	return nil
}

type Self struct{}

func (self *Self) IsLoggedIn(r *http.Request) bool {
	s, err := store.Get(r, "govwa")
	if err != nil {
		log.Println(err.Error())
	}
	if auth, ok := s.Values["govwa_session"].(bool); !ok || !auth {  // Missing Case if + short_var_declaration + binary_expression + unary_expression
		return false
	}
	return true
}

func (self *Self) SetSession(w http.ResponseWriter, r *http.Request, data map[string]string) {
	session, err := store.Get(r, "govwa")

	if err != nil {
		log.Println(err.Error())
	}

	session.Options = &sessions.Options{  // Missing Case unary_expression + composite_literal
		Path:     "/",
		MaxAge:   3600,
		HttpOnly: false, //set to false for xss :)
	}

	session.Values["govwa_session"] = true  // Missing Case index_expression + selector_expression

	//create new session to store on server side
	if data != nil {
		for key, value := range data {  // Missing Case for_range
			session.Values[key] = value  // Missing Case index_expression + selector_expression
		}
	}

	err = session.Save(r, w) //safe session and send it to client as cookie
	if err != nil {
		log.Println(err.Error())
	}
}


func CheckLevel(r *http.Request) bool {
	level := GetCookie(r, "Level")
	if level == "" || level == "low" {
		return false //set default level to low
	} else if level == "high" {
		return true //level == high
	} else {
		return false // level == low
	}
}

func Connect() (*sql.DB, error) {
	config := config.LoadConfig()

	var dsn string
	var db *sql.DB

	dsn = fmt.Sprintf("%s:%s@tcp(%s:%s)/", config.User, config.Password, config.Sqlhost, config.Sqlport)  // Missing Case selector_expression
	db, err := sql.Open("mysql", dsn)

	if err != nil {
		return nil, err
	}
	_, err = db.Exec("CREATE DATABASE IF NOT EXISTS " + config.Dbname)  // Missing Case selector_expression

	if err != nil {
		return nil, err
	} else {
		dsn = fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", config.User, config.Password, config.Sqlhost, config.Sqlport, config.Dbname)  // Missing Case selector_expression
		db, err = sql.Open("mysql", dsn)

		if err != nil {
			return nil, err

		}
	}
	return db, nil
}

func DeleteCookie(w http.ResponseWriter, cookies []string){
	for _,name := range cookies{  // Missing Case for_range
		cookie := &http.Cookie{  // Missing Case for_range unary_expression + composite_literal
			Name:     name,
			Value:    "",
			Expires: time.Unix(0, 0),
		}
		http.SetCookie(w, cookie)
	}
}

func GetOSVersion() string {
	switch os := runtime.GOOS; os{  // Missing Case switch + short_var_declaration
	case "darwin":   // Missing Case case
		return "OS X"
	case "linux":  // Missing Case case
		return "Linux"
	default:  // Missing Case default
		fmt.Printf("%s.", os)
	}
	return ""
}

func PrintVars() {
	var i, j int = 1, 2  // Missing Case assign same type to both vars
	k := 3
	c, python, java := true, false, "no!"
	fmt.Println(i, j, k, c, python, java)
}

func ForLoops() {
	var i, sum int  // Missing Case assign same type to both vars
	for i = 0; i<10; i++ {  // Missing Case for_statement
		fmt.Println("For with assignment")
	}

	for j := 0; j < 10; j++ {  // Missing Case for_statement
		sum += j
		fmt.Println("For with var declaration")
	}

	sum = 1
	for ; sum < 1000; {  // Missing Case for_statement
		sum += sum
		fmt.Println("For with condition only")
	}

	sum = 1
	for sum < 1000 {  // Missing Case for_statement
		sum += sum
		fmt.Println("For as while")
	}

	for {  // Missing Case for_statement
		fmt.Println("Continuous For")
	}
}
