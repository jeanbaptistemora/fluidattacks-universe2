import CommonCrypto
import IDZSwiftCommonCrypto
import CryptoSwift

import Crypto
import IDZSwiftCommonCrypto


let algorithm = CCAlgorithm(kCCAlgorithmDES) // Noncompliant: 64 bits block size

let algorithm = .des // Noncompliant: 64 bits block size

let blowfish = try Blowfish(key: key, blockMode: GCM(iv: iv, mode: .combined), padding: .pkcs7)
 // Noncompliant: 64 bits block size





let sealedBox = try AES.GCM.seal(input, using: key) // Compliant

let algorithm = CCAlgorithm(kCCAlgorithmAES) // Compliant

let algorithm = .aes // Compliant


let aes = try AES(key: key, iv: iv) // Compliant
