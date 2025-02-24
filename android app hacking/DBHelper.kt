package com.example.again
import android.annotation.SuppressLint
import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.provider.BaseColumns
class DBHelper(context: Context?, name:String?, factory:SQLiteDatabase.CursorFactory?, version: Int)
    : SQLiteOpenHelper(context, name, factory, version) {
    override fun onCreate(db: SQLiteDatabase?) {
        val sql: String = " CREATE TABLE IF NOT EXISTS MYTABLE( " +
                " SEQ INTEGER PRIMARY KEY AUTOINCREMENT, " +
                " ID TEXT, PASSWORD TEXT) "
        db?.execSQL(sql)
    }

    override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
        val sql: String = " DROP TABLE IF EXISTS MYTABLE"
        db?.execSQL(sql)
        onCreate(db)
    }

    fun insert(db: SQLiteDatabase, id: String, pw: String) {
        val sql = " INSERT INTO MYTABLE(ID, PASSWORD) VALUES ('${id}', '${pw}') "
        db?.execSQL(sql)
    }

    fun check(db: SQLiteDatabase, id: String): String? {
        val sql = "SELECT * FROM MYTABLE " +
                "WHERE ID = '${id}'"
        var result = db.rawQuery(sql, null)
        return result.getString(0)

    }

    }
