<template>
  <div>
    <el-row>
      <el-col :span="8">
        <!--@keyup.enter.native表示回车也调用handleSearch方法-->
        <!--搜索-->
        <el-input v-model="params.name"
                  placeholder="搜索书名"
                  @keyup.enter.native="handleSearch">
          <el-button slot="append"
                     icon="el-icon-search"
                     @click="handleSearch" />
        </el-input>
      </el-col>
      <el-col :span="16"
              style="text-align: right">
        <!--添加按钮-->
        <el-button v-if="addPerm"
                   type="primary"
                   @click="handleAddBtn">添加图书</el-button>
      </el-col>
    </el-row>
    <book-table :form="books"
                @edit="handleEdit"
                @delete="handleDelete" />

    <!--模态窗更新表单-->
    <el-dialog :visible.sync="dialogVisibleForEdit"
               title="更新图书信息"
               width="50%">
      <book-form ref="BookForm"
                 :form="currentValue"
                 @submit="handleSubmitEdit"
                 @cancel="handleCancelEdit" />
    </el-dialog>

    <!--模态窗增加表单-->
    <el-dialog :visible.sync="dialogVisibleForAdd"
               title="添加"
               width="50%"
               @close="handleCancelAdd">
      <BookForm ref="BookForm"
                @submit="handleSubmitAdd"
                @cancel="handleCancelAdd" />
    </el-dialog>

    <!--分页-->
    <center>
      <el-pagination :total="totalNum"
                     background
                     layout="total, prev, pager, next, jumper"
                     @current-change="handleChange" />
    </center>
  </div>
</template>

<script>
import { getBooksList, updateBooks,deleteBooks,createBooks } from "@/api/books/book"
import { checkPerms } from "@/utils/auth"
import BookTable from "./table.vue"
import BookForm from "./form.vue"
export default {
  name: "Books",
  components: {
    BookTable,
    BookForm
  },
  data () {
    return {
      params: {
        page: 1,
        name: "",
        authors: "",
        publisher: ""
      },
      totalNum: 0,
      books: [],
      dialogVisibleForEdit: false,
      dialogVisibleForAdd: false,
      currentValue: ""
    }
  },
  computed: {
    addPerm (perm) {
      return checkPerms("books.add_book")
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      getBooksList(this.params).then(res => {
        this.books = res.results
        this.totalNum = res.count
      })
    },
    handleEdit (Obj) { // 接收到的obj是所有的数据
      // console.log(Obj)
      this.currentValue = Obj
      // authors,publisher存入id,使用map方法
      this.currentValue["authors"] = this.currentValue["authors"].map(it => it.id)
      this.currentValue["publisher"] = this.currentValue["publisher"][0].id
      this.dialogVisibleForEdit = true
    },
    handleCancelEdit () {
      this.$refs.BookForm.$refs.form.resetFields()
      this.dialogVisibleForEdit = false
    },
    handleSubmitEdit (value) { // 更新的时候需要传一个id,接收到的value是所有的数据,需要把id和数据分开
      const { id, ...params } = value
      updateBooks(id, params).then(res => {
        this.$message({
          message: `修改出版商 ${params.name} 成功`,
          type: "success"
        })
        this.handleCancelEdit()
        this.fetchData()
      })
    },
    handleDelete (value) {
      deleteBooks(value.id).then(res => {
        this.$message({
          message: `删除图书 ${value.name} 成功`,
          type: "success"
        })
        this.fetchData()
      })
    },
    handleSearch () {
      this.fetchData()
    },
    handleAddBtn () {
      this.dialogVisibleForAdd = true
    },
    handleSubmitAdd (value) {
      createBooks(value).then(res => {
        this.$message({
          message: `添加图书 ${value.name} 成功`,
          type: "success"
        })
        this.handleCancelAdd()
        this.fetchData()
      })
    },
    handleCancelAdd () {
      this.$refs.BookForm.$refs.form.resetFields()
      this.dialogVisibleForAdd = false
    },
    handleChange (value) {
      this.params.page = value
      this.fetchData()
    }
  }
}
</script>
