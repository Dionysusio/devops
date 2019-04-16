<template>
  <div class="assign-group">
    <el-dialog :visible.sync="visible"
               title="指定角色"
               @close="handleClose">
      <el-form ref="addUserForm"
               label-width="100px">
        <el-form-item label="用户名：">
          <el-input v-model="userName"
                    readonly />
        </el-form-item>
        <el-form-item label="组名：">
          <el-select v-model="userGroups"
                     multiple
                     placeholder="请选择"
                     style="width:100%">
            <el-option v-for="item in options"
                       :key="item.id"
                       :label="item.name"
                       :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary">立即创建</el-button>
          <el-button>重置</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer"
           class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary"
                   @click="handleSubmit">提 交</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { getGroupList, updateUserGroups, getUserGroupList } from '@/api/group'
export default {
  name: 'AssignGroup',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    userId: {
      type: Number,
      default: 0
    },
    userName: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      visible: false,
      options: [],   // 所有组
      userGroups: [] // 存的是用户组的id
    }
  },
  watch: {
    value (val) {
      if (val <= 0) return
      this.visible = val
      this.fetchGroupList()  // 模态框展示的一瞬间获取组数据,所以在this.visible = val之后,调用fetchGroupList
      this.fetchUserGroups() // 当前用户的所有组
    }
  },
  methods: {
    handleClose () {
      // 关闭
      this.visible = false
      this.$emit('input', false)
      setTimeout(() => {
        this.options = []
        this.userGroups = []
      }, 500)
    },
    fetchGroupList () {
      // 获取所有组,保存到options里
      getGroupList({ page_size: 0 }).then(res => {
        this.options = res.results
        // 将数据保存到options里,不带分页的
      })
    },
    fetchUserGroups () {
      // 获取指定用户的所有组,保存到userGroups里,存的是id. page_size: 0 表示不分页,后端默认分页
      getUserGroupList(this.userId, { page_size: 0 }).then(res => {
        res.forEach((item) => {
          this.userGroups.push(item.id)
        })
      })
    },
    // 这样传多个参数时报错: TypeError: res.forEach is not a function
    handleSubmit () { // 提交,修改指定用户的角色,调用updateUserGroups
      // console.log(this.userGroups,this.userId)
      updateUserGroups(this.userId, { gids: this.userGroups }).then(() => {
        this.$message({
          message: `修改 ${this.userName} 用户组成功`,
          type: 'success'
        })
        this.handleClose() // 将模态框关闭
      })
    }
  }
}
</script>
