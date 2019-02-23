<template>
  <div>
    <el-table :data="form"
              style="width: 100%">
      <el-table-column type="index" />
      <el-table-column prop="name"
                       label="书名" />
      <el-table-column prop="publication_date"
                       label="出版时间" />
      <el-table-column prop="publisher"
                       label="出版社"
                       type="scope">
        <template slot-scope="scope">
          {{ scope.row.publisher[0].name }}
        </template>
      </el-table-column>
      <el-table-column prop="authors"
                       label="作者">
        <template slot-scope="scope">
          <div v-for="item in scope.row.authors"
               :key="item.id">
            <span style="float: left">{{ item.name }},</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column v-if="editPerm"
                       label="操作">
        <template slot-scope="scope">
          <el-button size="mini"
                     type="primary"
                     @click="handleEdit(scope.row)">编辑</el-button>

          <el-button v-if="deletePerm"
                     size="mini"
                     type="danger"
                     @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import { checkPerms } from '@/utils/auth'
export default {
  name: 'BookTable',
  props: {
    form: {
      type: Array,
      default () {
        return {
          name: '',
          publication_date: '',
          authors: '',
          publisher: ''
        }
      }
    }
  },
  computed: {
    editPerm () {
      return checkPerms('books.change_book')
    },
    deletePerm () {
      return checkPerms('books.delete_book')
    }
  },
  methods: {
    handleEdit (Obj) {
      this.$emit('edit', Obj)
    },
    handleDelete (Obj) {
      this.$emit('delete', Obj)
    }
  }
}
</script>
