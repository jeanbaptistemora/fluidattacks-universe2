package f073

import (
	"fmt"
)

func SwitchClause() {
	caseSwitch := 1
	switch caseSwitch {
		case 1:
			fmt.Println("Case 1")
		case 2:
			fmt.Println("Case 2")
		default:
			fmt.Println("Default Case")
	}
	switch caseSwitch {
		case 1:
			fmt.Println("Case 1")
		case 2:
			fmt.Println("Case 2")
	}
	switch caseSwitch.(type) {
		case int:
			fmt.Println("Case 1")
		case string:
			fmt.Println("Case 2")
		default:
			fmt.Println("Default Case")
	}
	switch caseSwitch.(type) {
		case int:
			fmt.Println("Case 1")
		case string:
			fmt.Println("Case 2")
	}
}
