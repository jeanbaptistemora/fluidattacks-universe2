Feature: Make coffee
  Coffee should brew after mixing the ingredients

  Background:
    Given a coffee pot
    And coffee beans
    And water

  Scenario: Make coffee from scratch
    When I grind the coffee
    Then I can put it in the pot
    When I put the coffee and water in the pot
    And I turn it on
    Then coffee should brew
