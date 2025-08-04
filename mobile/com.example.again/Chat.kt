package com.example.again
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import android.util.Log

class Chat {
    fun sendMessage(sender: String, message: String){
        val database = FirebaseDatabase.getInstance().getReference("chats")
        val messageId = database.push().key

        val chatMessage = ChatMessage(
            id = messageId ?: "",
            sender = sender,
            message = message
        )

        messageId?.let{
            database.child(it).setValue(chatMessage)
        }
    }

    fun receiveMessages(onNewMessage: (ChatMessage) -> Unit){
        val database = FirebaseDatabase.getInstance().getReference("chats")

        database.addValueEventListener(object: ValueEventListener{
            override fun onDataChange(snapshot: DataSnapshot) {
                for (data in snapshot.children) {
                    val message = data.getValue(ChatMessage::class.java)
                    message?.let{ onNewMessage(it)}
                }
            }

            override fun onCancelled(error: DatabaseError) {
                Log.e("Chat", "Failed to read messages", error.toException())
            }
        })
    }
}
