Imports System.Security.Cryptography
Imports System.Text
Public Class RSA
    Public Shared Function Encrypt(ByVal Data As String, ByVal Publickey As String) As RSAResult
        Try
            Dim ByteConverter As New UnicodeEncoding()
            Return Encrypt(ByteConverter.GetBytes(Data), Publickey)
        Catch ex As Exception
            Throw New Exception("Encrypt(String): " & ex.Message, ex)
        End Try
    End Function

    Public Shared Function Encrypt(ByVal Data() As Byte, ByVal Publickey As String) As RSAResult
        Try
            Dim RSA As System.Security.Cryptography.RSACryptoServiceProvider = New System.Security.Cryptography.RSACryptoServiceProvider(4096)
            RSA.FromXmlString(Publickey)
            Return New RSAResult(RSAEncrypt(Data, RSA.ExportParameters(False), False))
        Catch ex As Exception
            Throw New Exception("Encrypt(Bytes): " & ex.Message, ex)
        End Try
    End Function

    Public Shared Function Decrypt(ByVal Data() As Byte, ByVal Privatekey As String) As RSAResult
        Try
            Dim RSA As System.Security.Cryptography.RSACryptoServiceProvider = New System.Security.Cryptography.RSACryptoServiceProvider(4096)
            RSA.FromXmlString(Privatekey)
            Dim Result As New RSAResult(RSADecrypt(Data, RSA.ExportParameters(True), False))
            Return Result
        Catch ex As Exception
            Throw New Exception("Decrypt(): " & ex.Message, ex)
        End Try
    End Function

    Private Shared Function RSAEncrypt(ByVal DataToEncrypt() As Byte, ByVal RSAKeyInfo As RSAParameters, ByVal DoOAEPPadding As Boolean) As Byte()
        Try
            Dim encryptedData() As Byte
            Using RSA As New RSACryptoServiceProvider(4096)
                RSA.ImportParameters(RSAKeyInfo)
                encryptedData = RSA.Encrypt(DataToEncrypt, DoOAEPPadding)
            End Using
            Return encryptedData
        Catch e As CryptographicException
            Throw New Exception("RSAEncrypt(): " & e.Message, e)
        End Try
    End Function

    Private Shared Function RSADecrypt(ByVal DataToDecrypt() As Byte, ByVal RSAKeyInfo As RSAParameters, ByVal DoOAEPPadding As Boolean) As Byte()
        Try
            Dim decryptedData() As Byte
            Using RSA As New RSACryptoServiceProvider(4096)
                RSA.ImportParameters(RSAKeyInfo)
                decryptedData = RSA.Decrypt(DataToDecrypt, DoOAEPPadding)
            End Using
            Return decryptedData
        Catch e As CryptographicException
            Throw New Exception("RSADecrypt(): " & e.Message, e)
        End Try
    End Function
End Class
