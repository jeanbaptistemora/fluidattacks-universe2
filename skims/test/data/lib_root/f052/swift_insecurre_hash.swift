import CryptoSwift
let bytes:Array<UInt8> = [0x01, 0x02, 0x03]

let digest1 = input.md5() // Noncompliant

let digest2 = input.sha256() // Compliant
