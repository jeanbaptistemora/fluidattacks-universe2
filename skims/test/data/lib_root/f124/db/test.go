package db

import (
	"database/sql"
)

func DBQuery(message string, price float64, qty int) {
	sql.Exec(`INSERT INTO tbl $1, $2, $3`, message, price, qty)
}
