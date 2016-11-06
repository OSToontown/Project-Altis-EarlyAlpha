Imports System.Security.Cryptography
Public Class Keypair
    Private _Publickey As String = String.Empty
    Private _Privatekey As String = String.Empty
    Public Property Publickey() As String
        Get
            Return _Publickey
        End Get
        Set(ByVal value As String)
            _Publickey = value
        End Set
    End Property
    Public Property Privatekey() As String
        Get
            Return _Privatekey
        End Get
        Set(ByVal value As String)
            _Privatekey = value
        End Set
    End Property
    Public Shared Function CreateNewKeys() As Keypair
        Try
            Using RSA As New RSACryptoServiceProvider(4096)
                Dim Keys As New Keypair
                Keys.Privatekey = RSA.ToXmlString(True)
                Keys.Publickey = RSA.ToXmlString(False)
                Return Keys
            End Using
        Catch ex As Exception
            Throw New Exception("Keypair.CreateNewKeys():" & ex.Message, ex)
        End Try
    End Function
End Class
