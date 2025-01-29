//page.tsx (server component) is where we'll fetch data and render our table.

import { Payment, columns } from "./columns"
import { DataTable } from "./data-table"
import { VisualObject } from './columns'
import { getObjectsTest } from "@/lib/api"

async function getData(): Promise<VisualObject[]> {
    // Fetch data from your API here.

    const data = await getObjectsTest()
    return data
    /*return [
        {
            id: "728ed52f",
            amount: 100,
            status: "pending",
            email: "m@example.com",
        },
        {
            id: "728ed52f",
            amount: 100,
            status: "pending",
            email: "no@example.com",
        },
        {
            id: "728ed52f",
            amount: 100,
            status: "pending",
            email: "yxcv@example.com",
        },
        {
            id: "728ed52f",
            amount: 100,
            status: "pending",
            email: "a@example.com",
        },
        {
            id: "728ed52f",
            amount: 100,
            status: "pending",
            email: "ds@example.com",
        },
        // ...
    ]*/
}

export default async function DemoPage() {
    const data = await getData()

    return (
        <div className="container mx-auto py-10">
            <DataTable columns={columns} data={data} />
        </div>
    )
}
