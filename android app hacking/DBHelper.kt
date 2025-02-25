package com.example.again
import android.annotation.SuppressLint
import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.provider.BaseColumns
class DBHelper(context: Context)
    : SQLiteOpenHelper(context, "Login.db", null, 1) {
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

    fun insert(id: String, pw: String) {
        val db = this.writableDatabase
        val sql = db.rawQuery(" INSERT INTO MYTABLE(ID, PASSWORD) VALUES (?, ?) ", arrayOf(id, pw))
        val result = sql.moveToFirst()
        sql.close()
    }

    fun check(id: String): Boolean {
        val db = this.readableDatabase
        val sql = db.rawQuery("SELECT * FROM MYTABLE WHERE id = ?", arrayOf(id))
        var result = sql.moveToFirst()
        sql.close()
        return result
    }
    fun login(id: String, pw: String): Boolean{
        val db = this.readableDatabase
        println(db)
        val sql = db.rawQuery("SELECT * FROM MYTABLE WHERE id = ? and password = ?", arrayOf(id, pw))
        var result = sql.moveToFirst()
        sql.close()
        return result
    }

    }
