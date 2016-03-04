package main

type Article struct {
    Id  uint64  `db:"id",primarykey,autoincrement`
    Posted  int64   `db:"posted"`
    Link    string  `db:"url"`
    Feed    string  `db:"feed"`
}
