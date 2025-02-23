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
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val clickme = findViewById<Button>(R.id.click_me)
        val register = findViewById<TextView>(R.id.register)
        register.setOnClickListener{
            val intent = Intent(this, subActivity::class.java)
            startActivity(intent)
        }
        clickme.setOnClickListener{
            val value = findViewById<EditText>(R.id.password)
            if(value.text.toString() == "hacked"){
                Toast.makeText(this, "DH{y0u_a4e_a_h4ck3r!}", Toast.LENGTH_SHORT).show()
            }
            else
                Toast.makeText(this, "Button Clicked", Toast.LENGTH_SHORT).show()
        }
    }


}
