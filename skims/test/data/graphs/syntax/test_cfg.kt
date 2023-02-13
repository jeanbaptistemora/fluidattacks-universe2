package sast

import android.content.ContentProvider
import android.content.ContentValues
import android.content.Context
import android.content.UriMatcher
import android.database.SQLException
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.net.Uri
import android.support.v7.app.AppCompatActivity
import android.util.Log
import java.io.File
import java.io.FileOutputStream

const val SHIFT = 3

class AccountProvider : ContentProvider() {

    private lateinit var database: DatabaseHelper

    private val ACCOUNTS = 1
    private val ACCOUNTS_ID = 2

    private val sURIMatcher = UriMatcher(UriMatcher.NO_MATCH)

    init {
        sURIMatcher.addURI(AUTHORITY, ACCOUNTS_TABLE, ACCOUNTS)
        sURIMatcher.addURI(
            AUTHORITY, ACCOUNTS_TABLE + "/#", ACCOUNTS_ID
        )
    }

    override fun insert(uri: Uri, values: ContentValues): Uri? {
        val uriType = sURIMatcher.match(uri)

        val sqlDB = this.database.writableDatabase

        val id: Long
        when (uriType) {
            ACCOUNTS -> id = sqlDB.insert(ACCOUNTS_TABLE, null, values)
            else -> throw IllegalArgumentException("Unknown URI: " + uri)
        }
        context.contentResolver.notifyChange(uri, null)
        return Uri.parse(ACCOUNTS_TABLE + "/" + id)
    }

    companion object {
        private val AUTHORITY = "com.cx.vulnerablekotlinapp.accounts"
        private val ACCOUNTS_TABLE = "Accounts"
        val CONTENT_URI: Uri = Uri.parse(
            "content://" + AUTHORITY + "/" + ACCOUNTS_TABLE
        )
        private val DATABASE_NAME = "data"
    }
}

class CryptoHelper {
    companion object {
        fun encrypt(original: String): String {
            var encrypted: String = ""

            for (c in original) {
                val ascii: Int = c.toInt()
                val lowerBoundary: Int = if (c.isUpperCase()) 65 else 97

                if (ascii in 65..90 || ascii in 97..122) {
                    encrypted += ((ascii + SHIFT - lowerBoundary) % 26 + lowerBoundary).toChar()
                } else {
                    encrypted += c
                }
            }

            return encrypted
        }

        fun decrypt(encrypted: String): String {
            var original: String = ""

            for (c in encrypted) {
                val ascii: Int = c.toInt()
                val lowerBoundary: Int = if (c.isUpperCase()) 65 else 97

                if (ascii in 65..90 || ascii in 97..122) {
                    original += ((ascii - SHIFT - lowerBoundary) % 26 + lowerBoundary).toChar()
                } else {
                    original += c
                }
            }

            return original
        }
    }
}

class DatabaseHelper(val context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {
    private fun installDatabaseFromAssets() {
        val inputStream = context.assets.open("$ASSETS_PATH/$DATABASE_NAME.sqlite3")

        try {
            val outputFile = File(context.getDatabasePath(DATABASE_NAME).path)
            val outputStream = FileOutputStream(outputFile)

            inputStream.copyTo(outputStream)
            inputStream.close()

            outputStream.flush()
            outputStream.close()
        } catch (exception: Throwable) {
            throw RuntimeException("The $DATABASE_NAME database couldn't be installed.", exception)
        }
    }

    @Synchronized
    private fun installOrUpdateIfNecessary() {
        if (installedDatabaseIsOutdated()) {
            context.deleteDatabase(DATABASE_NAME)
            installDatabaseFromAssets()
            writeDatabaseVersionInPreferences()
        }
    }

    public fun createAccount(username: String, password: String): Boolean {
        val db: SQLiteDatabase = this.writableDatabase
        val record: ContentValues = ContentValues()
        var status = true

        record.put("username", username)
        record.put("password", password)

        try {
            db.insertOrThrow(TABLE_ACCOUNTS, null, record)
        } catch (e: SQLException) {
            Log.e("Database signup", e.toString())
            status = false
        } finally {
            return status
        }
    }

    companion object {
        const val ASSETS_PATH = "database"
        const val DATABASE_NAME = "data"
        const val DATABASE_VERSION = 4
        const val TABLE_ACCOUNTS = "Accounts"
        const val TABLE_NOTES = "Notes"
    }
}

class HomeActivity : AppCompatActivity() {
    private lateinit var listView: ListView
    private val apiService by lazy {
        Client.create()
    }

    private fun sync() {
        val username: String = PreferenceHelper.getString("userEmail", "")
        val account: Account = DatabaseHelper(applicationContext).getAccount(username)
        val basicAuth: String = Client.getBasicAuthorizationHeader(account.username, account.password)
        val cursor: Cursor = DatabaseHelper(applicationContext).listNotes(account.id)
        while (cursor.moveToNext()) {
            val id: Int = cursor.getInt(cursor.getColumnIndex("_id"))
            val title: String = cursor.getString(cursor.getColumnIndex("title"))
            val content: String = cursor.getString(cursor.getColumnIndex("content"))
            val createdAt: String = cursor.getString(cursor.getColumnIndex("createdAt"))
            val note: Note = Note(title, content, createdAt)

            val call: Call<Void> = apiService.syncNote(basicAuth, username, id, note)
            call.enqueue(object : Callback<Void> {
                override fun onFailure(call: Call<Void>, t: Throwable) {
                    Log.e("Sync", t.message.toString())
                }

                override fun onResponse(call: Call<Void>, response: Response<Void>) {
                    Log.i("Sync", "Note #$id: ${response.code()}")
                }
            })
        }
    }
}

class ServerInfoActivity : AppCompatActivity() {
    private lateinit var serverIPAddress: String
    private lateinit var serverPort: String
    val IP_ADDRESS = "ip_address"
    val PORT = "port"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_server_info)

        val prefs = applicationContext.getSharedPreferences(
            applicationContext.packageName, Context.MODE_PRIVATE
        )
        this.serverIPAddress = prefs!!.getString("ip_address", "127.0.0.1")
        this.serverPort = prefs!!.getString("port", "8080")

        var buttonSave: Button = findViewById(R.id.buttonSave)

        buttonSave.setOnClickListener {
            this.serverIPAddress = findViewById<EditText>(R.id.IPAddress).text.toString()
            this.serverPort = findViewById<EditText>(R.id.port).text.toString()

            if (
                this.serverIPAddress.isNullOrEmpty() or
                this.serverPort.isNullOrEmpty()
            ) {
                // Do nothing

                this.displayAlert()
            } else {
                val prefs = applicationContext.getSharedPreferences(
                    applicationContext.packageName, Context.MODE_PRIVATE
                )
                val editor = prefs!!.edit()
                editor.putString(this.IP_ADDRESS, this.serverIPAddress)
                editor.putString(this.PORT, this.serverPort)
                editor.apply()
            }
        }
    }

    private fun displayAlert() {
        val alert = Builder(this)
        // Builder
        with(alert) {
            setTitle("Error")
            setMessage("IP Address or Port setting is empty!")

            setPositiveButton("OK") {
                dialog, _ ->
                dialog.dismiss()
            }
        }

        // Dialog
        val dialog = alert.create()
        dialog.show()
    }
}
