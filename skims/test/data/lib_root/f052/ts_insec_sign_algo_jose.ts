import jose from "jose";

async function firstTest(): Promise<void> {
  const secret = new TextEncoder().encode(
    "cc7e0d44fd473002f1c42167459001140ec6389b7353f8088f4d9a95f2f596f2"
  );
  const alg = "HS256";

  const jwt = await new jose.SignJWT({ "urn:example:claim": true })
    .setProtectedHeader({ alg })
    .setIssuedAt()
    .setIssuer("urn:example:issuer")
    .setAudience("urn:example:audience")
    .setExpirationTime("2h")
    .sign(secret);

  console.log(jwt);
}

async function secondTest(): Promise<void> {
  const secret = new TextEncoder().encode(
    "cc7e0d44fd473002f1c42167459001140ec6389b7353f8088f4d9a95f2f596f2"
  );

  const jwt = await new jose.SignJWT({ "urn:example:claim": true })
    .setIssuedAt()
    .setIssuer("urn:example:issuer")
    .setAudience("urn:example:audience")
    .setProtectedHeader({ alg: "HS256" })
    .setExpirationTime("2h")
    .sign(secret);

  console.log(jwt);
}

// Following test is safe (No lines should be marked)
async function safeTestI(): Promise<void> {
  const secret = new TextEncoder().encode(
    "cc7e0d44fd473002f1c42167459001140ec6389b7353f8088f4d9a95f2f596f2"
  );
  const alg = "RS256";

  const jwt = await new jose.SignJWT({ "urn:example:claim": true })
    .setProtectedHeader({ alg })
    .setIssuedAt()
    .setIssuer("urn:example:issuer")
    .setAudience("urn:example:audience")
    .setExpirationTime("2h")
    .sign(secret);

  console.log(jwt);
}

// Following test is safe (No lines should be marked)
async function safe_test_ii(): Promise<void>  {
  const alg = "RS256";
  const pkcs8 = `-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDCFg4UrY5xtulv
/NXKmL1J4qI1SopAfTNMo3X7p+kJO7plqUYjzaztcre1qfh0m33Sm1Q8oPbO/GpP
MU1/HgcceytgJ/b4UwufVVMl9BrMDYG8moDBylbVupFQS3Ly1L9i/iFG9Z9A9xzY
Zzf799A45bnvNXL6s2glzvjiRvfQ2NDF0anTcnZLcYtC7ugq1IMM+ihAcPfw8Qw2
chN/SmP4qAM+PKaQwagmU7doqmmyN9u38AfoYZ1GCFhEs5TBBT6H6h9YdHeVtiIq
1c+fl03biSIfLrV7dUBD39gBmXBcL/30Ya3D82mCEUC4zg/UkOfQOmkmV3Lc8YUL
QZ8EJkBLAgMBAAECggEAVuVE/KEP6323WjpbBdAIv7HGahGrgGANvbxZsIhm34ls
VOPK0XDegZkhAybMZHjRhp+gwVxX5ChC+J3cUpOBH5FNxElgW6HizD2Jcq6t6LoL
YgPSrfEHm71iHg8JsgrqfUnGYFzMJmv88C6WdCtpgG/qJV1K00/Ly1G1QKoBffEs
+v4fAMJrCbUdCz1qWto+PU+HLMEo+krfEpGgcmtZeRlDADh8cETMQlgQfQX2VWq/
aAP4a1SXmo+j0cvRU4W5Fj0RVwNesIpetX2ZFz4p/JmB5sWFEj/fC7h5z2lq+6Bm
e2T3BHtXkIxoBW0/pYVnASC8P2puO5FnVxDmWuHDYQKBgQDTuuBd3+0tSFVEX+DU
5qpFmHm5nyGItZRJTS+71yg5pBxq1KqNCUjAtbxR0q//fwauakh+BwRVCPOrqsUG
jBSb3NYE70Srp6elqxgkE54PwQx4Mr6exJPnseM9U4K+hULllf5yjM9edreJE1nV
NVgFjeyafQhrHKwgr7PERJ/ikwKBgQDqqsT1M+EJLmI1HtCspOG6cu7q3gf/wKRh
E8tu84i3YyBnI8uJkKy92RNVI5fvpBARe3tjSdM25rr2rcrcmF/5g6Q9ImxZPGCt
86eOgO9ErNtbc4TEgybsP319UE4O41aKeNiBTAZKoYCxv/dMqG0j4avmWzd+foHq
gSNUvR2maQKBgQCYeqOsV2B6VPY7KIVFLd0AA9/dwvEmgAYLiA/RShDI+hwQ/5jX
uxDu37KAhqeC65sHLrmIMUt4Zdr+DRyZK3aIDNEAesPMjw/X6lCXYp1ZISD2yyym
MFGH8X8CIkstI9Faf9vf6PJKSFrC1/HA7wq17VCwrUzLvrljTMW8meM/CwKBgCpo
2leGHLFQFKeM/iF1WuYbR1pi7gcmhY6VyTowARFDdOOu8GXYI5/bz0afvCGvAMho
DJCREv7lC/zww6zCTPYG+HOj+PjXlJFba3ixjIxYwPvyEJiDK1Ge18sB7Fl8dHNq
C5ayaqCqN1voWYUdGzxU2IA1E/5kVo5O8FesJeOhAoGBAImJbZFf+D5kA32Xxhac
59lLWBCsocvvbd1cvDMNlRywAAyhsCb1SuX4nEAK9mrSBdfmoF2Nm3eilfsOds0f
K5mX069IKG82CMqh3Mzptd7e7lyb9lsoGO0BAtjho3cWtha/UZ70vfaMzGuZ6JmQ
ak6k+8+UFd93M4z0Qo74OhXB
-----END PRIVATE KEY-----`;
  const privateKey = await jose.importPKCS8(pkcs8, alg);

  const jwt = await new jose.SignJWT({ "urn:example:claim": true })
    .setProtectedHeader({ alg })
    .setIssuedAt()
    .setIssuer("urn:example:issuer")
    .setAudience("urn:example:audience")
    .setExpirationTime("2h")
    .sign(privateKey);

  console.log(jwt);
}
