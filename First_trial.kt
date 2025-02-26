package com.example.again

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.view.Window
import android.widget.Button
import android.widget.EditText

class First_trial : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        supportRequestWindowFeature(Window.FEATURE_NO_TITLE)
        setContentView(R.layout.activity_first_trial)
        val check = findViewById<Button>(R.id.successButton)
        check.setOnClickListener{
            var name = findViewById<EditText>(R.id.name)
            finish()
        }
    }
}
