<?php

class Test {
  public function testing() {
    try {
      throw new Exception();
    } catch (CustomException | Exception $e) {

    } catch (\Exception) {
    } catch (\Firebase\JWT\ExpiredException $e) {
    } catch (\Throwable) {

    } catch (Exception $e) {
    } catch (Firebase\JWT\ExpiredException $e) {
    } catch (Throwable) {
    }
  }
}

?>
