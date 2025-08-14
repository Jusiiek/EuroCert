export interface CreateUpdateTaskInterface {
    title: string;
    description?: string;
}

export interface TaskInterface extends CreateUpdateTaskInterface {
    _id: string;
}

