package f022

import org.apache.commons.net.ftp.FTPClient
import org.apache.commons.net.ftp.FTPSClient
import org.apache.commons.net.smtp.SMTPClient
import org.apache.commons.net.smtp.SMTPSClient
import org.apache.commons.net.telnet.TelnetClient

fun main() {
    val telnet = TelnetClient()

    val ftpClient = FTPClient()
    val ftpsClient = FTPSClient()

    val smtpClient = SMTPClient()
    val smtpsClient = SMTPSClient()

    val spec1: ConnectionSpec = ConnectionSpec.Builder(
        ConnectionSpec.CLEARTEXT
    )
    val spec2: ConnectionSpec = ConnectionSpec.Builder(
        ConnectionSpec.MODERN_TLS
    )
}
