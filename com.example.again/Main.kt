package com.example.again

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.content.Intent
import android.widget.TextView
import android.widget.EditText
import android.widget.Button
import androidx.recyclerview.widget.RecyclerView
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.firebase.FirebaseApp

class Main : AppCompatActivity() {
    private lateinit var editTextMessage: EditText
    private lateinit var buttonSend: Button
    private lateinit var recyclerView: RecyclerView
    private lateinit var chatAdapter: ChatAdapter
    private val chatMessages = mutableListOf<ChatMessage>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat)
        editTextMessage = findViewById(R.id.editTextMessage)
        buttonSend = findViewById(R.id.buttonSend)
        recyclerView = findViewById(R.id.recyclerView)

        chatAdapter = ChatAdapter(chatMessages)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = chatAdapter

        // 실시간 메시지 수신
        Chat().receiveMessages { message ->
            chatMessages.add(message)
            chatAdapter.notifyDataSetChanged()
        }

        // 메시지 전송 버튼 클릭 이벤트
        buttonSend.setOnClickListener {
            val message = editTextMessage.text.toString().trim()
            if (message.isNotEmpty()) {
                Chat().sendMessage("User1", message)
                editTextMessage.text.clear()
            }
        }

    }
}
