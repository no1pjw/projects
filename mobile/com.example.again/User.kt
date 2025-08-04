package com.example.again
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import android.util.Log
import com.google.firebase.firestore.FirebaseFirestore

class User {
    fun sendUserinfo(id: String, pw: String, name: String) {
        val firestore = FirebaseFirestore.getInstance()
        val user = User_info(
            id = id,
            password = pw,
            name = name
        )
        firestore.collection("user")
            .document(id)
            .set(user)
            .addOnSuccessListener {
                Log.d("Firestore", "User successfully added!")
            }
            .addOnFailureListener { e ->
                Log.e("Firestore", "Error adding user", e)
            }

    }
    fun check_name(id: String, callback: (String?) -> Unit){
        val firestore = FirebaseFirestore.getInstance()
        firestore.collection("user").whereEqualTo("id", id).get()
            .addOnSuccessListener { documents->
                val document = documents.documents[0]
                var name = document.getString("name")
                callback(name)
            }

    }
    fun check_duplicate(id : String, pw : String, isLogin :Boolean, callback : (Boolean) -> Unit) {
        val database = FirebaseFirestore.getInstance()
        if (!isLogin) {
            database.collection("user").whereEqualTo("id", id).get()
                .addOnSuccessListener { documents ->
                    if (!documents.isEmpty) {
                        callback(true)
                    } else {
                        callback(false)
                    }
                }
                .addOnFailureListener { e ->
                    Log.e("Firestore", "중복 확인 실패: ${e.message}")
                    callback(false)
                }
        }
        else{
            database.collection("user").whereEqualTo("id", id).get()
                .addOnSuccessListener { documents ->
                    if (!documents.isEmpty) {
                        val document = documents.documents[0]
                        val db_pw = document.getString("password")
                        println(db_pw)
                        println(pw)
                        if (db_pw == pw){
                            callback(true)
                        }
                        else {
                            callback(false)
                        }
                    } else {
                        callback(false)
                    }
                }
                .addOnFailureListener { e ->
                    Log.e("Firestore", "중복 확인 실패: ${e.message}")
                    callback(false)
                }
        }
    }

}
