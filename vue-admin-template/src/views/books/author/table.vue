<template>
  <div>
    <el-table :data="value"
              border
              stripe
              style="width: 100%">

      <el-table-column type="index" />

      <el-table-column label="名称"
                       prop="name" />

      <el-table-column label="城市"
                       prop="address" />

      <el-table-column label="email"
                       prop="email" />

      <el-table-column label="电话"
                       prop="phone" />

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini"
                     type="primary"
                     @click="handleEdit(scope.row)">编辑</el-button>

          <el-button size="mini"
                     type="danger"
                     @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>

    </el-table>
  </div>
</template>

<script>
export default {
  name: 'AuthorTable',
  props: {
    value: {
      type: Array,
      default () {
        return {
          name: '',
          address: '',
          email: '',
          phone: '',
          id: ''
        }
      }
    }
    // value: Array
  },
  methods: {
    handleEdit (value) {
      this.$emit('edit', value)
    },
    handleDelete (publish) {
      const id = publish.id
      const name = publish.name
      this.$confirm(`此操作将删除： ${name}, 是否继续？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', id)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>
