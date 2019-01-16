echo 'Excel帳票作成を開始します。'

# --- パラメータ取得 ---
#echo $Args[0]
#echo $Args[1]

#[DateTime]::ParseExact("20130209","yyyyMMdd",$null).ToString("yyyy")

# --- 定数定義 ---
[String] $OutPutPath = 'C:\KOGANE\REPORT_TEST' # 帳票出力ディレクトリ
[String] $TempleFilePath = 'C:\Program Files\WORK\休暇届フォーマット.xlsx' # テンプレートパス
[String] $NewFilePath = $OutPutPath + '\休暇届(' + ([DateTime]::Now.ToString('yyyyMMddHHmmss')) + ').xlsx' # 加工後パス
[String] $SheetName = '休暇届' # 帳票シート名
[String] $UserName = 'TestUser' # Excel操作ユーザー

# --- パラメータから固定値を抽出 ---
[String] $Boss = "中島 部長"
[String] $Leader = "リーダー"
[String] $Belong = "システム２部"
[String] $Name = $Args[0]
[String] $Reason = $Args[1]
[String] $Range = $Args[2]
[String] $Memo = "0900-111-2222"

# --- コピー先パス存在確認 ---
If(Test-Path -Path $NewFilePath){
    echo '出力ファイルが既に存在します。処理を中断します。'
    Exit;
}

# --- ファイルコピー、読み取り属性変更(ReadOnly解除) --- 
Copy-Item -Path $TempleFilePath -Destination $NewFilePath
Set-ItemProperty -Path $NewFilePath -Name IsReadOnly -Value $FALSE

# ---  Excelオブジェクト操作 ---
Try{
    [__ComObject] $Excel = New-Object -ComObject Excel.Application
    Try{
        [MarshalByRefObject] $Book = $Excel.Workbooks.Open($NewFilePath) # ブックオープン
        [MarshalByRefObject] $Sheet = $Book.Worksheets.Item($SheetName) # シート取得
        #$lastRowIndex = $Book.Worksheets.Item($SheetName).UsedRange.Rows.Count       # 最終行の行数取得
        #$lastColumnIndex = $Book.Worksheets.Item($SheetName).UsedRange.Columns.Count # 最終列の列数取得
        #echo $lastRowIndex
        #echo $lastColumnIndex

        # 各セルに項目値を設定(セルは名前で指定)
        #$Book.Worksheets.Item($SheetName).Cells.Item(6,1) = 2
        $Sheet.Range("A6").Value2 = $Boss # 上長
        $Sheet.Range("AL5").Value2 = [DateTime]::Now.ToString("yyyy") # 年
        $Sheet.Range("AT5").Value2 = [DateTime]::Now.ToString("MM") # 月
        $Sheet.Range("AY5").Value2 = [DateTime]::Now.ToString("dd") # 日
        $Sheet.Range("AI9").Value2 = $Belong # 所属
        $Sheet.Range("AI11").Value2 = $Name # 氏名

        $Sheet.Range("H16").Value2 = [DateTime]::Now.ToString("yyyy") # 開始年
        $Sheet.Range("O16").Value2 = [DateTime]::Now.ToString("MM") # 開始月
        $Sheet.Range("T16").Value2 = [DateTime]::Now.ToString("dd") # 開始日
        $Sheet.Range("AB16").Value2 = [DateTime]::Now.ToString("yyyy") # 終了年
        $Sheet.Range("AI16").Value2 = [DateTime]::Now.ToString("MM") # 終了月
        $Sheet.Range("AN16").Value2 = [DateTime]::Now.ToString("dd") # 終了日
        $Sheet.Range("AV16").Value2 = 1 # 日数

        $Sheet.CheckBoxes($Range).Value = 1 # 種類
        $Sheet.Range("H28").Value2 = $Reason + "のため" # 事由
        $Sheet.Range("H36").Value2 = $Memo # 備考
        $Sheet.Range("AW47").Value2 = $Leader # 担当者
    }Finally{
        $Book.Close($true)
    }
}Finally{
    $Excel.Quit()
}

echo 'Excel帳票作成を終了します。'