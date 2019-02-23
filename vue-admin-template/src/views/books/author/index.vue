<template>
  <div>
    <el-col :span="8">
      <!-- 搜索 -->
      <el-input v-model="params.name"
                placeholder="搜索"
                @keyup.enter.native="searchClick">
        <el-button slot="append"
                   icon="el-icon-search"
                   @click="searchClick" />
      </el-input>
    </el-col>

    <!--添加按钮-->
    <el-col :span="16"
            style="text-align: right">
      <el-button type="primary"
                 @click="handleAddBtn">添加作者</el-button>
    </el-col>

    <!-- 列表显示表格 -->
    <author-table :value="authors"
                  @delete="handleDelete"
                  @edit="handleEdit" />

    <!--模态窗更新表单-->
    <el-dialog :visible.sync="dialogVisibleForEdit"
               title="更新"
               width="50%">
      <author-form ref="AuthorForm"
                   :form="currentValue"
                   @submit="handleSubmitEdit"
                   @cancel="handleCancelEdit" />
    </el-dialog>

    <!--模态窗增加表单-->
    <el-dialog :visible.sync="dialogVisibleForAdd"
               title="添加"
               width="50%">
      <author-form ref="AuthorForm"
                   @submit="handleSubmitAdd"
                   @cancel="handleCancelAdd" />
    </el-dialog>

    <!--分页-->
    <center>
      <el-pagination :total="totalNum"
                     background
                     layout="total, prev, pager, next, jumper"
                     @current-change="handleCurrentChange" />
    </center>
  </div>
</template>

<script>
import {
  getAuthorList,
  DeleteAuthor,
  UpdateAuthor,
  CreateAuthor
} from "@/api/books/author"
import AuthorTable from "./table.vue"
import AuthorForm from "./form.vue"
export default {
  name: "Author",
  components: {
    AuthorTable,
    AuthorForm
  },
  data () {
    return {
      authors: [],
      params: {
        name: "",
        page: 1
      },
      totalNum: 0,
      currentValue: "",
      dialogVisibleForEdit: false,
      dialogVisibleForAdd: false
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      getAuthorList(this.params).then(res => {
        // console.log(res)
        this.authors = res.results
        this.totalNum = res.count
      })
    },
    handleCurrentChange (val) {
      this.params.page = val
      this.fetchData()
    },
    searchClick () {
      this.fetchData()
    },
    handleDelete (id) {
      DeleteAuthor(id).then(
        res => {
          this.$message({
            message: "删除作者成功",
            type: "success"
          })
          this.fetchData()
        },
        err => {
          console.log(err.message)
        }
      )
    },
    handleEdit (value) {
      this.currentValue = { ...value }
      this.dialogVisibleForEdit = true
      // console.log(this.currentValue)
    },
    handleSubmitEdit (value) {
      const { id, ...params } = value
      console.log(params)
      UpdateAuthor(id, params).then(res => {
        this.$message({
          message: "更新作者成功",
          type: "success"
        })
        this.handleCancelEdit()
        this.fetchData()
      })
    },
    handleCancelEdit () {
      this.currentValue = ""
      this.$refs.AuthorForm.$refs.form.resetFields()
      this.dialogVisibleForEdit = false
    },
    handleSubmitAdd (value) {
      // console.log(value)
      CreateAuthor(value).then(res => {
        this.$message({
          message: "创建成功",
          type: "success"
        })
        this.handleCancelAdd()
        this.fetchData()
      })
    },
    handleCancelAdd () {
      this.$refs.AuthorForm.$refs.form.resetFields()
      this.dialogVisibleForAdd = false
    },
    handleAddBtn () {
      this.dialogVisibleForAdd = true
    }
  }
}
</script>
