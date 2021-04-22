import {
  BaseEntity,
  Column,
  Entity,
  OneToMany,
  PrimaryGeneratedColumn,
  Unique,
} from "typeorm";
import { Ad } from ".";

@Entity()
export class Bot extends BaseEntity {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column("varchar")
  username!: string;

  @Column("timestamptz")
  dob!: Date;

  @Column("varchar")
  gender!: string;

  @Column("varchar")
  fName!: string;

  @Column("varchar")
  lName!: string;

  @Column("int")
  otherTermsCategory!: number;

  @Column("varchar")
  password!: string;

  @Column("float")
  locLat!: number;

  @Column("float")
  locLong!: number;

  @Column("varchar")
  type!: string;

  @OneToMany(() => Ad, (ad) => ad.bot)
  ads!: Ad[];
}
