package db

import (
	"database/sql"
)

type Transaction struct {
	Amount  float64
	Message string
}

func DBQuery(message string, price float64, qty int) {
	sql.Exec(`INSERT INTO tbl $1, $2, $3`, message, price, qty)
}

func DBQuery2(transaction Transaction) {
	sql.Exec(`INSERT INTO tbl $1, $2`, transaction.Amount, transaction.Message)
}
