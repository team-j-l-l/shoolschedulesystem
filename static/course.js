async function renderList() {
    let response = await fetch(`/api/course/info`);
    if (!response.ok) {
        console.error(response);
        return;
    }

    let data = await response.json();

    let tbodyEl = document.createElement("tbody");
    for (let item of data) {
        let trEl = document.createElement("tr");
        tbodyEl.append(trEl);

        let tdEl;
        tdEl = document.createElement("td");
        tdEl.innerText = item.cou_cno;
        tdEl.className = "col-cou_cno";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-cou_cname";
        tdEl.innerText = item.cou_cname;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-cou_credit";
        tdEl.innerText = item.cou_credit;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-cou_ctype";
        tdEl.innerText = item.cou_ctype;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "ctrlbar";
        tdEl.append(renderRecordCtrlbar(item));
        trEl.append(tdEl);
    }

    let tableEl = document.querySelector("#course-table");
    document.querySelector("#course-table > tbody").remove();
    tableEl.append(tbodyEl);
}

function renderRecordCtrlbar(item) {
    let ctrlbarEl = document.createElement("div");

    let editBtn = document.createElement("a");
    editBtn.className = "btn";
    editBtn.innerText = "修改";
    editBtn.onclick = (e) => {
        openEditDialog(item);
    };
    ctrlbarEl.append(editBtn);

    let delBtn = document.createElement("a");
    delBtn.className = "btn";
    delBtn.innerText = "删除";
    delBtn.onclick = (e) => {
        openComfirmationDialog({
            message: `确定要删除“${item.cou_cname}(#${item.cou_cno})”的信息？`,
            onOk: () => {
                (async () => {
                    let response = await fetch(`/api/course/${item.cou_cn}`, {
                        method: "DELETE",
                    });

                    if (!response.ok) {
                        console.error(response);
                    }

                    renderList();
                })();
            },
        });
    };
    ctrlbarEl.append(delBtn);

    return ctrlbarEl;
}

async function openEditDialog(item) {
    let dialog = document.querySelector(".course-editor");

    let dialogTitle = dialog.querySelector(".dialog-head");
    let form = dialog.querySelector("form");

    if (item) {
        dialogTitle.innerText = `修改课程信息 (#${item.cou_cn})`;
        form.elements.cou_cn.value = item.cou_cn ?? null;
        form.elements.cou_cno.value = item.cou_cno ?? "";
        form.elements.cou_cname.value = item.cou_cname ?? "";
        form.elements.cou_credit.value = item.cou_credit ?? "";
        form.elements.cou_ctype.value = item.cou_ctype ?? "";
    } else {
        dialogTitle.innerText = "新建课程信息";
        form.elements.cou_cn.value = null;
        form.elements.cou_cno.value = "";
        form.elements.cou_cname.value = "";
        form.elements.cou_credit.value = "";
        form.elements.cou_ctype.value = "";
    }

    if (dialog.classList.contains("open")) {
        dialog.classList.remove("open");
    } else {
        dialog.classList.add("open");
    }
}

async function renderEditDialog() {
    let newStudentBtn = document.querySelector(".paper #new-btn");
    newStudentBtn.onclick = (e) => {
        openEditDialog();
    };

    let dialog = document.querySelector(".course-editor");

    let form = dialog.querySelector("form");

    let close_btn = dialog.querySelector("#close-btn");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    close_btn.onclick = closeDialog;

    let save_btn = dialog.querySelector("#save-btn");
    save_btn.onclick = (e) => {
        let data = {
            cou_cn: form.elements.cou_cn.value,
            cou_cno: form.elements.cou_cno.value,
            cou_cname: form.elements.cou_cname.value,
            cou_credit: form.elements.cou_credit.value,
            cou_ctype: form.elements.cou_ctype.value,
        };

        if (!data.cou_cn) {
            // 异步执行POST请求操作
            (async () => {
                let response = await fetch("/api/course", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        } else {
            // 异步执行PUT请求操作
            (async () => {
                let response = await fetch(`/api/course/${data.cou_cn}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        }
    };
}

async function openComfirmationDialog({ message, onOk, onCancel }) {
    let dialog = document.querySelector(".comfirmation-dialog");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    let okBtn = dialog.querySelector("#ok-btn");
    okBtn.onclick = (e) => {
        if (typeof onOk === "function") {
            onOk();
        }

        closeDialog();
    };

    let cancelBtn = dialog.querySelector("#cancel-btn");
    cancelBtn.onclick = (e) => {
        if (typeof onCancel === "function") {
            onCancel();
        }

        closeDialog();
    };

    let messageEl = dialog.querySelector("#message");
    messageEl.innerText = message;

    dialog.classList.add("open");
}

document.addEventListener("DOMContentLoaded", (e) => {
    renderList();
    renderEditDialog();
});