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

class subActivity : AppCompatActivity() {
    public var id_list = mutableListOf<String>("dabyeol1234")
    public var pw_list = mutableListOf<String>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sub2)
        var id = ""
        var password = ""
        val register_id_repeat = findViewById<Button>(R.id.register_id_repeat)
        val register_click = findViewById<Button>(R.id.register_click)
        var id_checked = false
        register_id_repeat.setOnClickListener{
            id = findViewById<EditText>(R.id.id).text.toString()
            var Find = id_list.indexOf(id)
            if (id == ""){
                Toast.makeText(this, "아이디를 입력해주세요.", Toast.LENGTH_SHORT).show()
            }
            else if (Find >= 0) {
                Toast.makeText(this, "중복된 아이디가 존재합니다.", Toast.LENGTH_SHORT).show()
            }
            else {
                Toast.makeText(this, "사용 가능한 아이디입니다!", Toast.LENGTH_SHORT).show()
                id_checked = true
            }
        }
        register_click.setOnClickListener{
            if (id_checked == false){
                Toast.makeText(this,"아이디를 체크해주세요.", Toast.LENGTH_SHORT).show()
            }
            else {
                password = findViewById<EditText>(R.id.password).text.toString()
                var password_check = findViewById<EditText>(R.id.password_check).text.toString()
                if (password == "") {
                    Toast.makeText(this, "비밀번호를 입력해주세요.", Toast.LENGTH_SHORT).show()
                } else if (password_check == "") {
                    Toast.makeText(this, "비밀번호 확인을 해주세요.", Toast.LENGTH_SHORT).show()
                } else if (password != password_check) {
                    Toast.makeText(this, "비밀번호와 비밀번호 확인이 일치하지 않습니다. 다시 확인해주세요.", Toast.LENGTH_SHORT)
                        .show()
                } else {
                    id_list.add(id)
                    pw_list.add(password)
                    Toast.makeText(this, "회원가입에 성공하였습니다.", Toast.LENGTH_SHORT).show()
                    Thread.sleep(500)
                    val intent = Intent(this, MainActivity::class.java)
                    startActivity(intent)
                }
            }
        }
    }


}
