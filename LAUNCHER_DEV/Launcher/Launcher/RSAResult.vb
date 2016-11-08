Imports System.Text
Public Class RSAResult
    Private _Data() As Byte
    Public Sub New(ByVal Data() As Byte)
        _Data = Data
    End Sub
    Public ReadOnly Property AsBytes() As Byte()
        Get
            Return _Data
        End Get
    End Property
    Public ReadOnly Property AsString() As String
        Get
            Dim ByteConverter As New UnicodeEncoding()
            Return ByteConverter.GetString(_Data)
        End Get
    End Property
    Public ReadOnly Property AsBase64String() As String
        Get
            Return Convert.ToBase64String(_Data)
        End Get
    End Property
End Class