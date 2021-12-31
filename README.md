# kincone-send-attendance
send attendance data with use vagrant

### MEMO

**git** 管理下にサンプルファイルを **add** すると **ignore** しても変更を追跡してしまう

下記コマンドを実行し、除外するよう設定

```sh
$ git update-index --skip-worktree kincone/.kincone.user
$ git update-index --skip-worktree kincone/attendance.csv
```

除外から戻すときは

```sh
$ git update-index --no-skip-worktree kincone/.kincone.user
$ git update-index --no-skip-worktree kincone/attendance.csv
```
