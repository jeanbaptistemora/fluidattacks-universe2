package f124

import (
	"dabatase/sql"
	"db"
	"math"
	"strconv"
)

func DangerousFloat(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	sql.QueryRow(`INSERT INTO tbl $1`, amount)
}

func DangerousFloat2(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	DBQuerySameFile("Message", amount, 0)
}

func DangerousFloat3(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	db.DBQuery("Message", amount, 0)
}

func SafeFloat(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	if math.IsNaN(amount) || math.IsInf(amount, 0) {
		return "Not a valid value"
	}
	sql.QueryRow(`INSERT INTO tbl $1`, amount)
}

func SafeFloat2(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	if math.IsNaN(amount) || math.IsInf(amount, 0) {
		return "Not a valid value"
	}
	DBQuerySameFile("Message", amount, 0)
}

func SafeFloat3(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	if math.IsNaN(amount) || math.IsInf(amount, 0) {
		return "Not a valid value"
	}
	db.DBQuery("Message", amount, 0)
}

func DBQuerySameFile(message string, price float64, qty int) {
	sql.Exec(`INSERT INTO tbl $1, $2, $3`, message, price, qty)
}
