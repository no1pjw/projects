package com.example.again

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.view.View
import android.widget.Toast
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.content.Intent
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.io.Serializable

class User(var id : String, var pw : String): Serializable{
    constructor(): this("", "")
}

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        var dbHelper = DBHelper(this)
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val clickme = findViewById<Button>(R.id.click_me)
        val register = findViewById<TextView>(R.id.register)
        register.setOnClickListener{
            val intent = Intent(this, subActivity::class.java)
            startActivity(intent)
        }
        clickme.setOnClickListener{
            var id = findViewById<EditText>(R.id.id).text.toString()
            var password = findViewById<EditText>(R.id.password).text.toString()
            var Find = dbHelper.login(id, password)
            if(id == ""){
                Toast.makeText(this, this.getString(R.string.input_id), Toast.LENGTH_SHORT).show()
            }
            else if(password == ""){
                Toast.makeText(this, this.getString(R.string.input_password), Toast.LENGTH_SHORT).show()
            }
            else{
                if (Find){
                    Toast.makeText(this, this.getString(R.string.login_success), Toast.LENGTH_SHORT).show()
                    Thread.sleep(500)
                    val intent = Intent(this, MainActivity2::class.java)
                    startActivity(intent)
                }
                else{
                    Toast.makeText(this, this.getString(R.string.login_failed), Toast.LENGTH_SHORT).show()
                }
            }
        }
    }


}
