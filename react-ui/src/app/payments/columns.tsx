//(client component) will contain our column definitions.

"use client"

import { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"
import { MoreHorizontal } from "lucide-react"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
    id: string
    amount: number //visible
    status: "pending" | "processing" | "success" | "failed" //color
    email: string //type
}

// You can use a Zod schema here if you want.
export type VisualObject = {
    id: string
    name: string
    type: string  
    x: number
    y: number
    color: string
    scale_x: number
    scale_y: number
    border_width: number
    visible: boolean
}


export const columns: ColumnDef<VisualObject>[] = [
    {
        id: "select",
        header: ({ table }) => (
            <Checkbox
                checked={
                    table.getIsAllPageRowsSelected() ||
                    (table.getIsSomePageRowsSelected() && "indeterminate")
                }
                onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
                aria-label="Select all"
            />
        ),
        cell: ({ row }) => (
            <Checkbox
                checked={row.getIsSelected()}
                onCheckedChange={(value) => row.toggleSelected(!!value)}
                aria-label="Select row"
            />
        ),
    },
    {
        accessorKey: "id",
        header: "ID",
    },
    {
        accessorKey: "name",
        header: ({ column }) => {
            return (
                <Button
                    variant="ghost"
                    onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                >
                    Name
                    <ArrowUpDown className="ml-2 h-4 w-4" />
                </Button>
            )
        },
    },
    {
        accessorKey: "position",
        header: "Position",
        cell: ({ row }) => {
            // Kombiniere x und y zu einem String
            const x = row.original.x
            const y = row.original.y
            return `${x} x ${y}`; 
          },
    },
    {
        accessorKey: "size",
        header: "Größe",
        cell: ({ row }) => {
            // Kombiniere x und y zu einem String
            const x = row.original.scale_x
            const y = row.original.scale_y
            return `${x} x ${y}`; 
          },
    },
    {
        accessorKey: "border_width",
        header: "Umrandung",
    },
    {
        accessorKey: "type",
        header: "Form",
    },
    {
        accessorKey: "visible",
        header: "Visible",
    },
    {
        id: "actions",
        cell: ({ row }) => {
            const payment = row.original

            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Open menu</span>
                            <MoreHorizontal className="h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem
                            onClick={() => navigator.clipboard.writeText(payment.id)}
                        >
                            Copy payment ID
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>View customer</DropdownMenuItem>
                        <DropdownMenuItem>View payment details</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        },
    },
]
