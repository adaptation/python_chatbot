echo 'Excel���[�쐬���J�n���܂��B'

# --- �p�����[�^�擾 ---
#echo $Args[0]
#echo $Args[1]

#[DateTime]::ParseExact("20130209","yyyyMMdd",$null).ToString("yyyy")

# --- �萔��` ---
[String] $OutPutPath = 'C:\KOGANE\REPORT_TEST' # ���[�o�̓f�B���N�g��
[String] $TempleFilePath = 'C:\Program Files\WORK\�x�ɓ̓t�H�[�}�b�g.xlsx' # �e���v���[�g�p�X
[String] $NewFilePath = $OutPutPath + '\�x�ɓ�(' + ([DateTime]::Now.ToString('yyyyMMddHHmmss')) + ').xlsx' # ���H��p�X
[String] $SheetName = '�x�ɓ�' # ���[�V�[�g��
[String] $UserName = 'TestUser' # Excel���샆�[�U�[

# --- �p�����[�^����Œ�l�𒊏o ---
[String] $Boss = "���� ����"
[String] $Leader = "���[�_�["
[String] $Belong = "�V�X�e���Q��"
[String] $Name = $Args[0]
[String] $Reason = $Args[1]
[String] $Range = $Args[2]
[String] $Memo = "0900-111-2222"

# --- �R�s�[��p�X���݊m�F ---
If(Test-Path -Path $NewFilePath){
    echo '�o�̓t�@�C�������ɑ��݂��܂��B�����𒆒f���܂��B'
    Exit;
}

# --- �t�@�C���R�s�[�A�ǂݎ�葮���ύX(ReadOnly����) --- 
Copy-Item -Path $TempleFilePath -Destination $NewFilePath
Set-ItemProperty -Path $NewFilePath -Name IsReadOnly -Value $FALSE

# ---  Excel�I�u�W�F�N�g���� ---
Try{
    [__ComObject] $Excel = New-Object -ComObject Excel.Application
    Try{
        [MarshalByRefObject] $Book = $Excel.Workbooks.Open($NewFilePath) # �u�b�N�I�[�v��
        [MarshalByRefObject] $Sheet = $Book.Worksheets.Item($SheetName) # �V�[�g�擾
        #$lastRowIndex = $Book.Worksheets.Item($SheetName).UsedRange.Rows.Count       # �ŏI�s�̍s���擾
        #$lastColumnIndex = $Book.Worksheets.Item($SheetName).UsedRange.Columns.Count # �ŏI��̗񐔎擾
        #echo $lastRowIndex
        #echo $lastColumnIndex

        # �e�Z���ɍ��ڒl��ݒ�(�Z���͖��O�Ŏw��)
        #$Book.Worksheets.Item($SheetName).Cells.Item(6,1) = 2
        $Sheet.Range("A6").Value2 = $Boss # �㒷
        $Sheet.Range("AL5").Value2 = [DateTime]::Now.ToString("yyyy") # �N
        $Sheet.Range("AT5").Value2 = [DateTime]::Now.ToString("MM") # ��
        $Sheet.Range("AY5").Value2 = [DateTime]::Now.ToString("dd") # ��
        $Sheet.Range("AI9").Value2 = $Belong # ����
        $Sheet.Range("AI11").Value2 = $Name # ����

        $Sheet.Range("H16").Value2 = [DateTime]::Now.ToString("yyyy") # �J�n�N
        $Sheet.Range("O16").Value2 = [DateTime]::Now.ToString("MM") # �J�n��
        $Sheet.Range("T16").Value2 = [DateTime]::Now.ToString("dd") # �J�n��
        $Sheet.Range("AB16").Value2 = [DateTime]::Now.ToString("yyyy") # �I���N
        $Sheet.Range("AI16").Value2 = [DateTime]::Now.ToString("MM") # �I����
        $Sheet.Range("AN16").Value2 = [DateTime]::Now.ToString("dd") # �I����
        $Sheet.Range("AV16").Value2 = 1 # ����

        $Sheet.CheckBoxes($Range).Value = 1 # ���
        $Sheet.Range("H28").Value2 = $Reason + "�̂���" # ���R
        $Sheet.Range("H36").Value2 = $Memo # ���l
        $Sheet.Range("AW47").Value2 = $Leader # �S����
    }Finally{
        $Book.Close($true)
    }
}Finally{
    $Excel.Quit()
}

echo 'Excel���[�쐬���I�����܂��B'