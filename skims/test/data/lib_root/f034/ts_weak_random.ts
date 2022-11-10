import { Router } from "express";

const router = Router();
function routa(req, res) {
  let key = Math.random().toString();
  res.cookie("rememberKey", key);
  res.json({ ok: true });
}
router.get("/test148", routa);

export default router;
