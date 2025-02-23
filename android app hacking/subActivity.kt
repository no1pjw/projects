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
    public val id_list = mutableListOf<Int>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sub2)

    }


}
