function vuln (req, res) {
    const value = req.query.value;

    res.setHeader("Set-Cookie", value);  // Noncompliant
    res.cookie("connect.sid", value);  // Noncompliant

    res.setHeader("X-Data", value); // Compliant
    res.cookie("data", value); // Compliant
  };
