package com.example.again

import androidx.recyclerview.widget.RecyclerView
import android.widget.TextView
import android.view.View
import android.view.ViewGroup
import android.view.LayoutInflater


class ChatAdapter(private val messages: List<ChatMessage>) :
    RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {

    class ChatViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val textViewMessage: TextView = view.findViewById(R.id.textViewMessage)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_chat_message, parent, false)
        return ChatViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        holder.textViewMessage.text = messages[position].message
    }

    override fun getItemCount(): Int = messages.size
}
