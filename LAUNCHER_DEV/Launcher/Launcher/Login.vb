Imports System.Text
Imports System.Threading
Imports System.ComponentModel
Imports System.Security.Cryptography
Imports System.IO
Imports System.Management

''' <summary>
''' TO DO:
''' Launch game with token
''' </summary>
''' <remarks></remarks>

Public Class Login
    Private neededResources As String() = {"TTAltis.EXE", "TTAltisdata.bin", "phase_3.mf", "phase_3.5.mf", "phase_4.mf", "phase_5.mf", "phase_6.mf", "phase_7.mf", "phase_8.mf", "phase_9.mf", "phase_10.mf", "phase_11.mf", "phase_12.mf", "phase_13.mf"} ' "stage_3.mf", "stage_4.mf"}
    Const ip As String = "127.0.0.1" '"188.165.250.225"
    Const port As UShort = 1337
    Private HWID As String
    Private WithEvents client As New UserClient
    Private serverOnline As Boolean = False
    Private encrypted As Boolean = False
    Private serverPubKey As String
    Private PrivateKey As String
    Private PublicKey As String
    Private AESKey As String
    Private status As Integer
    Private downloadList As New SortedSet(Of String)
    Private Delegate Sub DoDownload()
    Private playable As Boolean = False
    Private hashes As SortedList(Of String, String) 'File as Key, Hash as Value

    Enum statusKey As Integer
        Heartbeat = 0
        Transmission = 1
        KeyExchange = 2
        Encrypted = 3
    End Enum


    Private Sub ITalk_TextBox_Small1_MouseEnter(sender As Object, e As EventArgs) Handles ITalk_TextBox_Small1.MouseEnter
        If ITalk_TextBox_Small1.Text = "Username" Then
            ITalk_TextBox_Small1.Text = ""
            ITalk_TextBox_Small2.Text = ""
        End If
    End Sub

    Private Sub Login_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        getHWID()
        My.Computer.Audio.Play(My.Resources.Launcher_Theme, AudioPlayMode.BackgroundLoop)
        CreateNewKeys()
        client.KeepAlive = True
        client.Connect(ip, port)
        System.Threading.Thread.Sleep(2000)
        status = statusKey.Heartbeat
        sendToServer("PING")
    End Sub

    Private Function getHWID()
        Dim HWID As String = String.Empty
        Dim mcl As New ManagementClass("win32_processor")
        Dim MOBC As ManagementObjectCollection = mcl.GetInstances()

        For Each mob As ManagementObject In MOBC
            If HWID = "" Then
                HWID = mob.Properties("processorID").Value.ToString()
                Exit For
            End If
        Next
        Return HWID
    End Function

    Private Sub handlePacket(ByRef data() As Byte)
        Select Case DirectCast(status, statusKey)
            Case statusKey.Heartbeat
                If Encoding.ASCII.GetString(data) = "PONG" Then
                    serverOnline = True
                    status = statusKey.Transmission
                    sendToServer("STARTENC")
                End If
            Case statusKey.Transmission
                Dim text() As String = Encoding.ASCII.GetString(data).Split("#")
                serverPubKey = text(1)
                sendToServer("KEY#" & PublicKey)
                status = statusKey.KeyExchange

            Case statusKey.KeyExchange
                Dim text As String = RSAdecryptMessage(data)
                If text = "NEXT" Then
                    sendToServer("AES#" & AESKey)
                ElseIf text = "DONE" Then
                    status = statusKey.Encrypted
                End If

            Case statusKey.Encrypted
                Dim text As String = AES_Decrypt(Encoding.ASCII.GetString(data), AESKey)
                If text.Contains("TKN") Then
                    Dim token As String = text.Split("#")(1)
                    'YAY! PLAY TOKEN AUTHORIZED

                    'Remove all Login UI Components

                    ITalk_TextBox_Small1.Visible = False
                    ITalk_TextBox_Small2.Visible = False
                    KnightButton1.Visible = False

                    'Prepare for download

                    ITalk_Button_21.Visible = True



                    If Not IO.Directory.Exists(FileIO.SpecialDirectories.ProgramFiles + "\Project Altis\") Then
                        IO.Directory.CreateDirectory(FileIO.SpecialDirectories.ProgramFiles + "\Project Altis\")
                    End If


                    For Each file As String In neededResources


                        If Not FileIO.FileSystem.FileExists(FileIO.SpecialDirectories.ProgramFiles & "\Project Altis\" & file) Then
                            downloadList.Add(file)
                        Else
                            'Check hash and work out if you need to re-download and re-hash
                            Dim localHash As String = genSHA(FileIO.SpecialDirectories.ProgramFiles & "\Project Altis\" & file)
                            Using wc As New Net.WebClient
                                Dim result As String = wc.DownloadString("http://gs1.ToontownAltis.com/live/hashCheck.php?file=" & file & "&hash=" & localHash)
                                If Not result = "Valid" Then
                                    downloadList.Add(file)
                                    FileIO.FileSystem.DeleteFile(FileIO.SpecialDirectories.ProgramFiles & "\Project Altis\" & file)
                                End If
                            End Using
                        End If
                    Next

                    For i As Integer = 0 To downloadList.Count - 1
                        ITalk_Button_21.Text = "Now Downloading " & downloadList(i).ToString
                        Application.DoEvents()
                        'client.DownloadFile(New Uri("http://" & ip & "/tt2/live/" & downloadList(i)), FileIO.SpecialDirectories.ProgramFiles & "\Project Altis\" & downloadList(i))
                        Try
                            My.Computer.Network.DownloadFile("http://gs1.ToontownAltis.com/live/" & downloadList(i), FileIO.SpecialDirectories.ProgramFiles & "\Project Altis\" & downloadList(i), vbNullString, vbNullString, True, 5000, True)
                        Catch ex As Exception
                            'User Clicked Cancel NOT DOWNLOADED
                        End Try

                    Next


                    MsgBox(token)
                    My.Computer.Audio.Stop()
                    'RUN THE GAME

                ElseIf text = "BADLOGIN" Then
                    'OH NO! WE'VE BEEN REJECTED
                    MonoFlat_NotificationBox2.Text = "I'm sorry! It looks like that Username/Password combination is not recognised! Try typing it in again or reset your password on our website!"
                    MonoFlat_NotificationBox2.Visible = True
                ElseIf text = "LOGINCLOSED" Then
                    MonoFlat_NotificationBox3.Text = "I'm sorry! An administrator has temporarily disabled logins! Please try again later!"
                    MonoFlat_NotificationBox3.Visible = True
                End If
        End Select
    End Sub


    Private Sub client_ReadPacket(sender As UserClient, data() As Byte) Handles client.ReadPacket
        handlePacket(data)
    End Sub

    Private Sub CreateNewKeys()
        Dim Keys As Keypair = Keypair.CreateNewKeys
        PrivateKey = Keys.Privatekey
        PublicKey = Keys.Publickey
        AESKey = generateAESKey()
    End Sub

    Public Function generateAESKey() As String
        Dim s As String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        Dim r As New Random
        Dim sb As New StringBuilder
        For i As Integer = 1 To 256
            Dim idx As Integer = r.Next(0, 35)
            sb.Append(s.Substring(idx, 1))
        Next
        Return sb.ToString()
    End Function

    Public Function genSHA(ByRef fileToHash As String)
        Dim hash = SHA1.Create()
        Dim hashValue() As Byte
        Dim fileStream As FileStream = File.OpenRead(fileToHash)
        fileStream.Position = 0
        hashValue = hash.ComputeHash(fileStream)
        Dim hash_hex = PrintByteArray(hashValue)
        fileStream.Close()
        Return hash_hex
    End Function

    Public Function PrintByteArray(ByVal array() As Byte)
        Dim hex_value As String = ""
        Dim i As Integer
        For i = 0 To array.Length - 1
            hex_value += array(i).ToString("X2")
        Next i
        Return hex_value.ToLower
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
            Dim decryptedMessage As RSAResult = RSA.Decrypt(bytesToDecrypt, PrivateKey)
            Dim decryptedString As String = Encoding.ASCII.GetString(decryptedMessage.AsBytes)
            Return decryptedString
        Catch ex As Exception
            Return ""
        End Try
    End Function

    Private Sub sendToServer(ByRef text As String)
        Select Case DirectCast(status, statusKey)
            Case statusKey.Heartbeat
                client.Send(Encoding.ASCII.GetBytes("PING"))

            Case statusKey.Transmission
                client.Send(Encoding.ASCII.GetBytes(text))

            Case statusKey.KeyExchange
                client.Send(RSAencryptMessage(text, serverPubKey))

            Case statusKey.Encrypted
                client.Send(Encoding.ASCII.GetBytes(AES_Encrypt(text, AESKey)))

        End Select
    End Sub

    Private Sub KnightButton1_Click(sender As Object, e As EventArgs) Handles KnightButton1.Click
        If Not serverOnline Then
            MonoFlat_NotificationBox1.Text = "We've been un-able to connect to the auth server at the moment! Please try again in a few minutes or check your internet connection!"
            MonoFlat_NotificationBox1.Visible = True
            client.Connect(ip, port)
            sendToServer("")
        Else
            MonoFlat_NotificationBox1.Visible = False
            If status = statusKey.Encrypted Then
                sendToServer("LGN#" & ITalk_TextBox_Small1.Text.ToString & "#" & ITalk_TextBox_Small2.Text.ToString & "#" & HWID)
                MonoFlat_NotificationBox2.Visible = False
                MonoFlat_NotificationBox3.Visible = False
                MonoFlat_NotificationBox1.Visible = False
            End If
        End If
    End Sub

    Private Sub FlatButton1_Click(sender As Object, e As EventArgs)
        client.Connect(ip, port)
    End Sub
End Class
