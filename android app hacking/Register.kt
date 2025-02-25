package com.example.again

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.Toast
import android.widget.Button
import android.widget.EditText
import android.content.Intent
import java.util.regex.Pattern

class Register : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)
        var dbHelper = DBHelper(this)
        var id = ""
        var password = ""
        var email = ""
        val register_id_repeat = findViewById<Button>(R.id.register_id_repeat)
        val register_click = findViewById<Button>(R.id.register_click)
        val register_email_check = findViewById<Button>(R.id.register_email_check)
        var id_checked = false
        register_id_repeat.setOnClickListener{
            id = findViewById<EditText>(R.id.id).text.toString()
            if (id == ""){
                Toast.makeText(this, this.getString(R.string.input_id), Toast.LENGTH_SHORT).show()
            }
            else if(Pattern.matches("^[a-zA-Z0-9]*&", id) && id.length >= 6){
                var Find = dbHelper.check(id)
                if (Find){
                    Toast.makeText(this, this.getString(R.string.is_id_duplicated), Toast.LENGTH_SHORT).show()
                }
                else{
                    Toast.makeText(this, this.getString(R.string.useable_id), Toast.LENGTH_SHORT).show()
                    id_checked = true
                }
            }
            else {
                Toast.makeText(this, this.getString(R.string.wrong_id), Toast.LENGTH_LONG).show()
            }
        }
        register_email_check.setOnClickListener{
        }
        register_click.setOnClickListener{
            if (id_checked == false){
                Toast.makeText(this,this.getString(R.string.check_id), Toast.LENGTH_SHORT).show()
            }
            else {
                password = findViewById<EditText>(R.id.password).text.toString()
                var password_check = findViewById<EditText>(R.id.password_check).text.toString()
                if (password == "") {
                    Toast.makeText(this, this.getString(R.string.input_password), Toast.LENGTH_SHORT).show()
                } else if (password_check == "") {
                    Toast.makeText(this, this.getString(R.string.check_password), Toast.LENGTH_SHORT).show()
                } else if (password != password_check) {
                    Toast.makeText(this, this.getString(R.string.password_match_false), Toast.LENGTH_SHORT)
                        .show()
                } else {
                    val result = dbHelper.insert(id, password)
                    Toast.makeText(this, "회원가입에 성공하였습니다.", Toast.LENGTH_SHORT).show()
                    Thread.sleep(500)
                    val intent = Intent(this, Login::class.java)
                    startActivity(intent)
                }
            }
        }
    }


}
