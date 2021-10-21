<?php

class Test {
  public function testing() {
    try {
      throw new Exception();
    } catch (CustomException | Exception $e) {
    } catch (Exception $e) {
    }
  }
}

?>
