<?php

class Test {
  public function testing() {
    try {
      throw new Exception();
    } catch (Exception $e) {
    }
  }
}

?>
