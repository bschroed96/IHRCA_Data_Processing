$files = Get-ChildItem -Path '.\country_lists'
$langs = Import-Csv -Path '.\langs.csv'


foreach ($f in $files) {
    foreach ($lang in $langs) {
        if ($f.Name -match $lang.language) {
            python3 main.py $f.Name $lang.code
        }
    }

}