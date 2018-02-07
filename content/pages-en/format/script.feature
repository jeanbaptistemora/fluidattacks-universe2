Feature: Make coffee
  Coffee should brew after mixing the ingredients

  Background:       
    Given a cofee pot
    And coffee beans
    And water

  Scenario: Make coffee from scratch
    When I grind the coffee
    Then I can put in in the pot
    When I put the cofee and water in the pot
    When I turn it on
    Then coffee should brew

