package f127

import (
	"dabatase/sql"
	"math"
	"strconv"
)

func Dangerous(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	sql.QueryRow(`INSERT INTO tbl $1`, amount)
}

func Dangerous2(request *http.Request) {
	amount = strconv.ParseFloat(request.Amount)
	sql.Exec(`INSERT INTO tbl $1, $2, $3`, amount)
}

func SafeMethod(request *http.Request) {
	amount := strconv.ParseFloat(request.Amount)
	if math.IsNaN(amount) || math.IsInf(amount, 0) {
		return "Not a valid value"
	}
	sql.QueryCol(`INSERT INTO tbl $1`, amount)
}
