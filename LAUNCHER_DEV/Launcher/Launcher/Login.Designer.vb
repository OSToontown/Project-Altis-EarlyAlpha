<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Login
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        Me.BackgroundWorker1 = New System.ComponentModel.BackgroundWorker()
        Me.ITalk_Button_21 = New Launcher.iTalk.iTalk_Button_2()
        Me.MonoFlat_NotificationBox3 = New Launcher.MonoFlat.MonoFlat_NotificationBox()
        Me.MonoFlat_NotificationBox2 = New Launcher.MonoFlat.MonoFlat_NotificationBox()
        Me.MonoFlat_NotificationBox1 = New Launcher.MonoFlat.MonoFlat_NotificationBox()
        Me.KnightButton1 = New Launcher.KnightButton()
        Me.ITalk_TextBox_Small2 = New Launcher.iTalk.iTalk_TextBox_Small()
        Me.ITalk_TextBox_Small1 = New Launcher.iTalk.iTalk_TextBox_Small()
        Me.PictureBox1 = New System.Windows.Forms.PictureBox()
        Me.PictureBox2 = New System.Windows.Forms.PictureBox()
        CType(Me.PictureBox1, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.PictureBox2, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'BackgroundWorker1
        '
        Me.BackgroundWorker1.WorkerReportsProgress = True
        '
        'ITalk_Button_21
        '
        Me.ITalk_Button_21.BackColor = System.Drawing.Color.FromArgb(CType(CType(0, Byte), Integer), CType(CType(152, Byte), Integer), CType(CType(224, Byte), Integer))
        Me.ITalk_Button_21.Font = New System.Drawing.Font("Segoe UI", 14.0!)
        Me.ITalk_Button_21.ForeColor = System.Drawing.Color.White
        Me.ITalk_Button_21.Image = Nothing
        Me.ITalk_Button_21.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft
        Me.ITalk_Button_21.Location = New System.Drawing.Point(263, 527)
        Me.ITalk_Button_21.Name = "ITalk_Button_21"
        Me.ITalk_Button_21.Size = New System.Drawing.Size(533, 40)
        Me.ITalk_Button_21.TabIndex = 8
        Me.ITalk_Button_21.Text = "Preparing Download"
        Me.ITalk_Button_21.TextAlignment = System.Drawing.StringAlignment.Center
        Me.ITalk_Button_21.Visible = False
        '
        'MonoFlat_NotificationBox3
        '
        Me.MonoFlat_NotificationBox3.BorderCurve = 8
        Me.MonoFlat_NotificationBox3.Font = New System.Drawing.Font("Tahoma", 9.0!)
        Me.MonoFlat_NotificationBox3.Image = Nothing
        Me.MonoFlat_NotificationBox3.Location = New System.Drawing.Point(263, 351)
        Me.MonoFlat_NotificationBox3.MinimumSize = New System.Drawing.Size(100, 40)
        Me.MonoFlat_NotificationBox3.Name = "MonoFlat_NotificationBox3"
        Me.MonoFlat_NotificationBox3.NotificationType = Launcher.MonoFlat.MonoFlat_NotificationBox.Type.[Error]
        Me.MonoFlat_NotificationBox3.RoundCorners = False
        Me.MonoFlat_NotificationBox3.ShowCloseButton = False
        Me.MonoFlat_NotificationBox3.Size = New System.Drawing.Size(533, 65)
        Me.MonoFlat_NotificationBox3.TabIndex = 6
        Me.MonoFlat_NotificationBox3.Visible = False
        '
        'MonoFlat_NotificationBox2
        '
        Me.MonoFlat_NotificationBox2.BorderCurve = 8
        Me.MonoFlat_NotificationBox2.Font = New System.Drawing.Font("Tahoma", 9.0!)
        Me.MonoFlat_NotificationBox2.Image = Nothing
        Me.MonoFlat_NotificationBox2.Location = New System.Drawing.Point(263, 351)
        Me.MonoFlat_NotificationBox2.MinimumSize = New System.Drawing.Size(100, 40)
        Me.MonoFlat_NotificationBox2.Name = "MonoFlat_NotificationBox2"
        Me.MonoFlat_NotificationBox2.NotificationType = Launcher.MonoFlat.MonoFlat_NotificationBox.Type.Notice
        Me.MonoFlat_NotificationBox2.RoundCorners = False
        Me.MonoFlat_NotificationBox2.ShowCloseButton = False
        Me.MonoFlat_NotificationBox2.Size = New System.Drawing.Size(533, 65)
        Me.MonoFlat_NotificationBox2.TabIndex = 5
        Me.MonoFlat_NotificationBox2.Visible = False
        '
        'MonoFlat_NotificationBox1
        '
        Me.MonoFlat_NotificationBox1.BorderCurve = 8
        Me.MonoFlat_NotificationBox1.Font = New System.Drawing.Font("Tahoma", 9.0!)
        Me.MonoFlat_NotificationBox1.Image = Nothing
        Me.MonoFlat_NotificationBox1.Location = New System.Drawing.Point(263, 351)
        Me.MonoFlat_NotificationBox1.MinimumSize = New System.Drawing.Size(100, 40)
        Me.MonoFlat_NotificationBox1.Name = "MonoFlat_NotificationBox1"
        Me.MonoFlat_NotificationBox1.NotificationType = Launcher.MonoFlat.MonoFlat_NotificationBox.Type.Warning
        Me.MonoFlat_NotificationBox1.RoundCorners = False
        Me.MonoFlat_NotificationBox1.ShowCloseButton = False
        Me.MonoFlat_NotificationBox1.Size = New System.Drawing.Size(533, 65)
        Me.MonoFlat_NotificationBox1.TabIndex = 4
        Me.MonoFlat_NotificationBox1.Visible = False
        '
        'KnightButton1
        '
        Me.KnightButton1.Location = New System.Drawing.Point(395, 291)
        Me.KnightButton1.Name = "KnightButton1"
        Me.KnightButton1.RoundedCorners = False
        Me.KnightButton1.Size = New System.Drawing.Size(276, 54)
        Me.KnightButton1.TabIndex = 3
        Me.KnightButton1.Text = "Login"
        '
        'ITalk_TextBox_Small2
        '
        Me.ITalk_TextBox_Small2.BackColor = System.Drawing.Color.Transparent
        Me.ITalk_TextBox_Small2.Font = New System.Drawing.Font("Tahoma", 11.0!)
        Me.ITalk_TextBox_Small2.ForeColor = System.Drawing.Color.DimGray
        Me.ITalk_TextBox_Small2.Location = New System.Drawing.Point(395, 237)
        Me.ITalk_TextBox_Small2.MaxLength = 32767
        Me.ITalk_TextBox_Small2.Multiline = False
        Me.ITalk_TextBox_Small2.Name = "ITalk_TextBox_Small2"
        Me.ITalk_TextBox_Small2.ReadOnly = False
        Me.ITalk_TextBox_Small2.Size = New System.Drawing.Size(276, 28)
        Me.ITalk_TextBox_Small2.TabIndex = 2
        Me.ITalk_TextBox_Small2.Text = "Password"
        Me.ITalk_TextBox_Small2.TextAlignment = System.Windows.Forms.HorizontalAlignment.Left
        Me.ITalk_TextBox_Small2.UseSystemPasswordChar = True
        '
        'ITalk_TextBox_Small1
        '
        Me.ITalk_TextBox_Small1.BackColor = System.Drawing.Color.Transparent
        Me.ITalk_TextBox_Small1.Font = New System.Drawing.Font("Tahoma", 11.0!)
        Me.ITalk_TextBox_Small1.ForeColor = System.Drawing.Color.DimGray
        Me.ITalk_TextBox_Small1.Location = New System.Drawing.Point(395, 183)
        Me.ITalk_TextBox_Small1.MaxLength = 32767
        Me.ITalk_TextBox_Small1.Multiline = False
        Me.ITalk_TextBox_Small1.Name = "ITalk_TextBox_Small1"
        Me.ITalk_TextBox_Small1.ReadOnly = False
        Me.ITalk_TextBox_Small1.Size = New System.Drawing.Size(276, 28)
        Me.ITalk_TextBox_Small1.TabIndex = 1
        Me.ITalk_TextBox_Small1.Text = "Username"
        Me.ITalk_TextBox_Small1.TextAlignment = System.Windows.Forms.HorizontalAlignment.Left
        Me.ITalk_TextBox_Small1.UseSystemPasswordChar = False
        '
        'PictureBox1
        '
        Me.PictureBox1.Dock = System.Windows.Forms.DockStyle.Fill
        Me.PictureBox1.Image = Global.Launcher.My.Resources.Resources.background
        Me.PictureBox1.Location = New System.Drawing.Point(0, 0)
        Me.PictureBox1.Name = "PictureBox1"
        Me.PictureBox1.Size = New System.Drawing.Size(1059, 598)
        Me.PictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        Me.PictureBox1.TabIndex = 0
        Me.PictureBox1.TabStop = False
        '
        'PictureBox2
        '
        Me.PictureBox2.BackColor = System.Drawing.Color.Transparent
        Me.PictureBox2.BackgroundImage = Global.Launcher.My.Resources.Resources.toontown_logo
        Me.PictureBox2.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
        Me.PictureBox2.Location = New System.Drawing.Point(395, 12)
        Me.PictureBox2.Name = "PictureBox2"
        Me.PictureBox2.Size = New System.Drawing.Size(276, 136)
        Me.PictureBox2.TabIndex = 9
        Me.PictureBox2.TabStop = False
        '
        'Login
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(1059, 598)
        Me.Controls.Add(Me.PictureBox2)
        Me.Controls.Add(Me.ITalk_Button_21)
        Me.Controls.Add(Me.MonoFlat_NotificationBox3)
        Me.Controls.Add(Me.MonoFlat_NotificationBox2)
        Me.Controls.Add(Me.MonoFlat_NotificationBox1)
        Me.Controls.Add(Me.KnightButton1)
        Me.Controls.Add(Me.ITalk_TextBox_Small2)
        Me.Controls.Add(Me.ITalk_TextBox_Small1)
        Me.Controls.Add(Me.PictureBox1)
        Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
        Me.Name = "Login"
        Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        Me.Text = "                                                                                 " &
    "                                                                                " &
    "      Project Altis"
        CType(Me.PictureBox1, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.PictureBox2, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)

    End Sub
    Friend WithEvents PictureBox1 As System.Windows.Forms.PictureBox
    Friend WithEvents ITalk_TextBox_Small1 As Launcher.iTalk.iTalk_TextBox_Small
    Friend WithEvents ITalk_TextBox_Small2 As Launcher.iTalk.iTalk_TextBox_Small
    Friend WithEvents KnightButton1 As Launcher.KnightButton
    Friend WithEvents MonoFlat_NotificationBox1 As Launcher.MonoFlat.MonoFlat_NotificationBox
    Friend WithEvents Timer1 As System.Windows.Forms.Timer
    Friend WithEvents ITalk_Button_21 As Launcher.iTalk.iTalk_Button_2
    Friend WithEvents BackgroundWorker1 As System.ComponentModel.BackgroundWorker
    Friend WithEvents MonoFlat_NotificationBox3 As MonoFlat.MonoFlat_NotificationBox
    Friend WithEvents MonoFlat_NotificationBox2 As MonoFlat.MonoFlat_NotificationBox
    Friend WithEvents PictureBox2 As PictureBox
End Class
