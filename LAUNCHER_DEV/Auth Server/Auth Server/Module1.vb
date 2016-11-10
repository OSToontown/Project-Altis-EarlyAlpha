Imports BCrypt.Net.BCrypt
Imports MySql.Data.MySqlClient
Imports System.Text


Module Module1
    Private WithEvents server As New ServerListener
    Private allClients As New List(Of ServerClient) ' Master List of All Clients
    Private authorizedClients As New List(Of ServerClient) ' Clients that are Encrypting their Traffic (Can Send/Receive Tokens/Passwords Respectivley)
    Private rsaClients As New SortedList(Of ServerClient, String) ' Client | Public Key
    Private aesClients As New SortedList(Of ServerClient, String) ' Client | Their AES Key
    Private DBConnection As New MySqlConnection()
    Private serverPrivateKey As String
    Private serverPublicKey As String
    Private serverAESKey As String
    Const port As String = "1337"
    Const ip As String = "127.0.0.1"
    Const user As String = "root"
    Const pass As String = ""

    Enum LogTypes As Integer
        Normal = 0 'White
        Warning = 1 'Yellow
        Success = 2 'Green
        Acknowledge = 3 'Cyan
        Critical = 4 'Red
        Security = 5 'Blue
    End Enum

    Sub Main()
        CreateNewKeys()
        connectToDB()
        server.KeepAlive = True
        server.Listen(port)

        While True
            server.Listen(port)
        End While
        Console.ReadLine()
    End Sub

    Private Function checkAccount(ByRef username As String, ByRef passwordToTry As String, ByRef endpoint As ServerClient) As String
        Try
            DBConnection.Open()
            Dim MyAdapter As New MySqlDataAdapter
            Dim SqlQuery = "SELECT * FROM ttdb.account WHERE username = """ & username & """;"
            Dim UpdateQuery = "SELECT * FROM ttdb.account WHERE username = """ & username & """;"
            Dim Command As New MySqlCommand
            Command.Connection = DBConnection
            Command.CommandText = SqlQuery
            MyAdapter.SelectCommand = Command
            Dim Mydata As MySqlDataReader
            Mydata = Command.ExecuteReader
            If Mydata.HasRows = 0 Then
                logMessage(1, "Unable to Retreive Data")
                logMessage(3, "Login Unsuccessful for {0}.", username)
                endpoint.Send(Encoding.ASCII.GetBytes(AES_Encrypt("BADLOGIN", aesClients(endpoint))))
            Else
                logMessage(2, "Data Retrieval Successful")
                Mydata.Read()
                Dim hash As String = Mydata.Item(2)
                Dim token As String = Mydata.Item(6)
                If BCrypt.Net.BCrypt.Verify(passwordToTry, hash) Then
                    logMessage(2, "Login Successful for {0}.", username)
                    'Don't send Token yet, try to make a new token. If it can't update DB, then disallow login and keep Token safe.
                    Try
                        DBConnection.Close()
                        DBConnection.Open()
                        Dim myCommand As New MySqlCommand
                        Dim SQL As String
                        myCommand.Connection = DBConnection
                        MyAdapter.SelectCommand = myCommand
                        SQL = "UPDATE ttdb.account SET Token = '" & genToken() & "' WHERE Username = '" & username & "'; "
                        SQL &= "UPDATE ttdb.account SET lastIP = '" & endpoint.EndPoint.Address.ToString & "' WHERE Username = '" & username & "';"
                        myCommand.CommandText = SQL
                        myCommand.ExecuteNonQuery()
                        logMessage(2, "Updated Play Token for {0}", username)



                        endpoint.Send(Encoding.ASCII.GetBytes(AES_Encrypt("TKN#" & token, aesClients(endpoint))))


                        logMessage(2, "Sent Play Token to {0}", username)
                    Catch ex As Exception
                        logMessage(1, "Unable to Update Play Token. Rejecting Login for {0}", username)
                        endpoint.Send(Encoding.ASCII.GetBytes(AES_Encrypt("LOGINCLOSED", aesClients(endpoint))))
                    End Try
                Else
                    logMessage(3, "Login Unsuccessful for {0}.", username)
                    endpoint.Send(Encoding.ASCII.GetBytes(AES_Encrypt("BADLOGIN", aesClients(endpoint))))
                    Return ""
                End If
            End If
            DBConnection.Dispose()
        Catch ex As Exception
            Console.WriteLine(ex)
        End Try
        
        Return ""
    End Function


    Private Sub connectToDB()
        Try
            DBConnection.ConnectionString = "server=" & ip & ";" & "user id=" & user & ";" & "password=" & pass & ";" & "database=ttdb"
            DBConnection.Open()
            logMessage(2, "Connected to the Database!")
        Catch ex As Exception
            logMessage(4, "{0}", ex)
        Finally
            DBConnection.Dispose()
        End Try
    End Sub

    Private Sub logMessage(ByRef type As Integer, ByRef message As String, ParamArray args As Object())
        If type = 0 Then
            Console.ForegroundColor = ConsoleColor.White
            Console.Write("Log: ")
        ElseIf type = 1 Then
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.Write("Warning: ")
        ElseIf type = 2 Then
            Console.ForegroundColor = ConsoleColor.Green
            Console.Write("Success: ")
        ElseIf type = 3 Then
            Console.ForegroundColor = ConsoleColor.Cyan
            Console.Write("Acknowledgment: ")
        ElseIf type = 4 Then
            Console.ForegroundColor = ConsoleColor.Red
            Console.Write("Error: ")
        ElseIf type = 5 Then
            Console.ForegroundColor = ConsoleColor.Blue
            Console.Write("Security: ")
        End If
        Console.WriteLine(String.Format(message, args))
    End Sub

    Private Function genToken()
        Dim s As String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        Dim r As New Random
        Dim sb As New StringBuilder
        For i As Integer = 1 To 46
            Dim idx As Integer = r.Next(0, 35)
            sb.Append(s.Substring(idx, 1))
        Next
        Return sb.ToString()
    End Function





    Private Sub CreateNewKeys()
        Dim Keys As Keypair = Keypair.CreateNewKeys
        serverPrivateKey = Keys.Privatekey
        serverPublicKey = Keys.Publickey
    End Sub

    Public Function generateAESKey() As String
        Static Generator As System.Random = New System.Random()
        Return Generator.Next(9999999, 2000000000)
    End Function

    Public Function AES_Encrypt(ByVal input As String, ByVal pass As String) As String
        Dim AES As New System.Security.Cryptography.RijndaelManaged
        Dim Hash_AES As New System.Security.Cryptography.MD5CryptoServiceProvider
        Dim encrypted As String = ""
        Try
            Dim hash(31) As Byte
            Dim temp As Byte() = Hash_AES.ComputeHash(System.Text.ASCIIEncoding.ASCII.GetBytes(pass))
            Array.Copy(temp, 0, hash, 0, 16)
            Array.Copy(temp, 0, hash, 15, 16)
            AES.Key = hash
            AES.Mode = Security.Cryptography.CipherMode.ECB
            Dim DESEncrypter As System.Security.Cryptography.ICryptoTransform = AES.CreateEncryptor
            Dim Buffer As Byte() = System.Text.ASCIIEncoding.ASCII.GetBytes(input)
            encrypted = Convert.ToBase64String(DESEncrypter.TransformFinalBlock(Buffer, 0, Buffer.Length))
            Return encrypted
        Catch ex As Exception
            Return ""
        End Try
    End Function

    Public Function AES_Decrypt(ByVal input As String, ByVal pass As String) As String
        Dim AES As New System.Security.Cryptography.RijndaelManaged
        Dim Hash_AES As New System.Security.Cryptography.MD5CryptoServiceProvider
        Dim decrypted As String = ""
        Try
            Dim hash(31) As Byte
            Dim temp As Byte() = Hash_AES.ComputeHash(System.Text.ASCIIEncoding.ASCII.GetBytes(pass))
            Array.Copy(temp, 0, hash, 0, 16)
            Array.Copy(temp, 0, hash, 15, 16)
            AES.Key = hash
            AES.Mode = Security.Cryptography.CipherMode.ECB
            Dim DESDecrypter As System.Security.Cryptography.ICryptoTransform = AES.CreateDecryptor
            Dim Buffer As Byte() = Convert.FromBase64String(input)
            decrypted = System.Text.ASCIIEncoding.ASCII.GetString(DESDecrypter.TransformFinalBlock(Buffer, 0, Buffer.Length))
            Return decrypted
        Catch ex As Exception
            Return ""
        End Try
    End Function

    Private Function RSAencryptMessage(ByRef textToEncrypt As String, ByRef publicKey As String) As Byte()
        Try
            Dim encryptedMessage As RSAResult = RSA.Encrypt(Encoding.ASCII.GetBytes(textToEncrypt), publicKey)
            Dim encryptedBytes As Byte() = encryptedMessage.AsBytes
            Return encryptedBytes
        Catch ex As Exception
            Return Encoding.ASCII.GetBytes("")
        End Try
    End Function

    Private Function RSAdecryptMessage(ByRef bytesToDecrypt As Byte()) As String
        Try
            Dim decryptedMessage As RSAResult = RSA.Decrypt(bytesToDecrypt, serverPrivateKey)
            Dim decryptedString As String = Encoding.ASCII.GetString(decryptedMessage.AsBytes)
            Return decryptedString
        Catch ex As Exception
            Return ""
        End Try
    End Function

    Private Sub handlePacket(ByRef client As ServerClient, ByRef data() As Byte)

        If Encoding.ASCII.GetString(data) = "PING" Then
            client.Send(Encoding.ASCII.GetBytes("PONG"))
        ElseIf Encoding.ASCII.GetString(data) = "STARTENC" Then
            client.Send(Encoding.ASCII.GetBytes("KEY#" & serverPublicKey))
        ElseIf Encoding.ASCII.GetString(data).Contains("KEY#") Then
            Dim text() As String = Encoding.ASCII.GetString(data).Split("#")
            rsaClients.Add(client, text(1))
            client.Send(RSAencryptMessage("NEXT", rsaClients(client)))
        ElseIf RSAdecryptMessage(data).Contains("AES#") Then
            Dim text() As String = RSAdecryptMessage(data).Split("#")
            aesClients.Add(client, text(1))
            client.Send(RSAencryptMessage("DONE", rsaClients(client)))
            authorizedClients.Add(client)
        ElseIf AES_Decrypt(Encoding.ASCII.GetString(data), aesClients(client)).Contains("LGN") Then
            Dim text() As String = AES_Decrypt(Encoding.ASCII.GetString(data), aesClients(client)).Split("#")
            Dim usernameToTry As String = text(1)
            Dim passwordToTry As String = text(2) 'Pass is hashed, but we can use BCrypts compare function
            checkAccount(usernameToTry, passwordToTry, client) : Exit Sub
        End If


    End Sub

    Private Sub handleConnectionStates(ByRef client As ServerClient, ByRef connected As Boolean)
        If connected = True Then
            If Not allClients.Contains(client) Then
                allClients.Add(client)
            End If
        Else
            If allClients.Contains(client) Then
                allClients.Remove(client)
            End If
            If authorizedClients.Contains(client) Then
                allClients.Remove(client)
            End If
            If aesClients.ContainsKey(client) Then
                aesClients.Remove(client)
            End If
            If rsaClients.ContainsKey(client) Then
                rsaClients.Remove(client)
            End If
        End If
    End Sub

    Private Sub server_ClientReadPacket(sender As ServerListener, client As ServerClient, data() As Byte) Handles server.ClientReadPacket
        handlePacket(client, data)
        Console.WriteLine("Received Packet")
    End Sub

    Private Sub server_ClientStateChanged(sender As ServerListener, client As ServerClient, connected As Boolean) Handles server.ClientStateChanged
        handleConnectionStates(client, connected)
    End Sub
End Module
